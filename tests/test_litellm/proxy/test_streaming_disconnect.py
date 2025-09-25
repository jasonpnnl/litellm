from __future__ import annotations

import asyncio
import datetime
from types import SimpleNamespace
from typing import Any, List
from unittest.mock import AsyncMock

import pytest

import litellm
from litellm.litellm_core_utils.litellm_logging import Logging as LiteLLMLoggingObj
from litellm.proxy.hooks.proxy_track_cost_callback import _ProxyDBLogger
from litellm.proxy.proxy_server import _finalize_stream_logging
from litellm.types.utils import CallTypes


class RecordingLogging(LiteLLMLoggingObj):
    def __init__(self) -> None:
        super().__init__(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "hi"}],
            stream=True,
            call_type=CallTypes.completion.value,
            start_time=datetime.datetime.now(),
            litellm_call_id="call-id",
            function_id="function-id",
            kwargs={},
        )
        self.async_calls: List[Any] = []
        self.sync_calls: List[Any] = []
        self.model_call_details["cache_hit"] = False

    async def async_success_handler(  # type: ignore[override]
        self, result=None, start_time=None, end_time=None, cache_hit=None, **kwargs
    ) -> None:
        self.async_calls.append((result, cache_hit))

    def success_handler(  # type: ignore[override]
        self, result=None, start_time=None, end_time=None, cache_hit=None, **kwargs
    ) -> None:
        self.sync_calls.append((result, cache_hit))


def test_finalize_stream_logging_delegates_to_logging_helper():
    logging_obj = SimpleNamespace(
        async_finalize_stream_from_chunks=AsyncMock()
    )
    response_stream = object()
    chunks = [object()]

    asyncio.run(
        _finalize_stream_logging(
            response_stream=response_stream,
            logging_obj=logging_obj,
            reason="client_disconnect",
            cancelled=True,
            collected_chunks=chunks,
        )
    )

    logging_obj.async_finalize_stream_from_chunks.assert_awaited_once_with(  # type: ignore[attr-defined]
        response_stream=response_stream,
        collected_chunks=chunks,
        reason="client_disconnect",
        cancelled=True,
    )


def test_async_finalize_stream_from_chunks_sets_metadata_and_calls_handlers(monkeypatch):
    recording_logger = RecordingLogging()

    dummy_choice = SimpleNamespace(finish_reason=None)
    assembled_response = SimpleNamespace(choices=[dummy_choice])

    def _fake_stream_chunk_builder(**kwargs):
        return assembled_response

    monkeypatch.setattr(litellm, "stream_chunk_builder", _fake_stream_chunk_builder)

    result = asyncio.run(
        recording_logger.async_finalize_stream_from_chunks(
            response_stream=None,
            collected_chunks=[SimpleNamespace()],
            reason="client_disconnect",
            cancelled=True,
        )
    )

    assert result is assembled_response
    assert recording_logger.model_call_details["stream_finalize_reason"] == "client_disconnect"
    assert recording_logger.model_call_details["stream_cancelled"] is True
    assert dummy_choice.finish_reason == "cancelled"
    assert recording_logger.async_calls
    assert recording_logger.sync_calls


def test_proxy_db_logger_stream_finalize_adds_metadata():
    logger = _ProxyDBLogger()
    kwargs: dict[str, Any] = {"litellm_params": {"metadata": {"preexisting": "value"}}}

    asyncio.run(
        logger.async_stream_finalize_event(
            kwargs=kwargs,
            response_obj=None,
            reason="client_disconnect",
            cancelled=True,
        )
    )

    metadata = kwargs["litellm_params"]["metadata"]
    assert metadata["stream_finalize_reason"] == "client_disconnect"
    assert metadata["stream_cancelled"] is True
    assert metadata["preexisting"] == "value"
