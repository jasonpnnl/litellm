#!/usr/bin/env python3
"""
Test script to verify streaming disconnection handling works correctly.
This will start a streaming request and cancel it mid-stream to test logging.

USAGE:
1. Start LiteLLM proxy server with --debug flag to see detailed logs
2. Run: python test_streaming_disconnect.py
3. Look for these debug messages in proxy logs:
   - "Client disconnected during streaming, continuing to consume stream for logging"
   - "Stream completed - client disconnected but logging should have occurred"
4. Verify request appears in Request Logs and spend tracking
"""
import asyncio
import aiohttp
import sys

async def test_streaming_disconnect():
    """Test that cancelling a streaming request still logs properly"""

    # Construct the request
    url = "http://localhost:4000/chat/completions"
    headers = {
        "Authorization": "Bearer sk-1234",  # Replace with your actual test key
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",  # Replace with an available model in your config
        "messages": [{"role": "user", "content": "Write a long story about space exploration. Include details about different planets and make it at least 500 words so there are many streaming chunks."}],
        "stream": True,
        "temperature": 0.7
    }

    print("🚀 Starting streaming request to test disconnection handling...")
    print("📝 This simulates a client pressing Ctrl+C during a streaming response")
    print()

    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data, headers=headers) as response:
                print(f"✅ Response status: {response.status}")
                if response.status != 200:
                    print(f"❌ Error response: {await response.text()}")
                    return

                chunk_count = 0
                async for chunk in response.content.iter_chunked(1024):
                    chunk_count += 1
                    chunk_text = chunk.decode('utf-8', errors='ignore')

                    # Print first part of each chunk
                    if 'data:' in chunk_text:
                        lines = chunk_text.strip().split('\n')
                        for line in lines:
                            if line.startswith('data:') and not line.startswith('data: [DONE]'):
                                print(f"📨 Chunk {chunk_count}: {line[:80]}...")
                                break

                    # Simulate client disconnection after receiving several chunks
                    if chunk_count >= 5:
                        print(f"\n🔴 SIMULATING CLIENT DISCONNECTION (Ctrl+C after {chunk_count} chunks)")
                        print("   In a real scenario, the client would close the connection here")
                        break

    except Exception as e:
        print(f"⚠️  Request cancelled/failed: {type(e).__name__}: {e}")

    print("\n✅ Test completed!")
    print("\n🔍 CHECK PROXY LOGS FOR:")
    print("   1. 'Client disconnected during streaming, continuing to consume stream for logging'")
    print("   2. 'Stream completed - client disconnected but logging should have occurred'")
    print("   3. Request should appear in Request Logs UI")
    print("   4. Spend should be tracked in /spend/logs API")
    print("\n💡 If you see these messages, the fix is working correctly!")

async def test_normal_streaming():
    """Test that normal streaming still works correctly"""

    url = "http://localhost:4000/chat/completions"
    headers = {
        "Authorization": "Bearer sk-1234",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Say hello and explain what you are in exactly 3 sentences."}],
        "stream": True
    }

    print("🧪 Testing normal streaming (should complete normally)...")

    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=data, headers=headers) as response:
                chunk_count = 0
                async for chunk in response.content.iter_chunked(1024):
                    chunk_count += 1
                    chunk_text = chunk.decode('utf-8', errors='ignore')

                    if 'data: [DONE]' in chunk_text:
                        print(f"✅ Normal streaming completed successfully after {chunk_count} chunks")
                        break

    except Exception as e:
        print(f"❌ Normal streaming failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "normal":
        asyncio.run(test_normal_streaming())
    else:
        print("Testing disconnection scenario...")
        asyncio.run(test_streaming_disconnect())
        print("\nTo test normal streaming, run: python test_streaming_disconnect.py normal")