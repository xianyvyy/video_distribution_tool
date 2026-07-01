"""
Platform adapter tests: base interface, each adapter returns correct types.
"""
import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))


def test_bilibili_adapter_upload_requires_credential():
    from adapter.bilibili_adapter import BilibiliAdapter
    from adapter.base_adapter import UploadResult
    adapter = BilibiliAdapter()
    assert adapter.platform_name == "bilibili"
    r = adapter.upload_video("/fake/path", "title", credential=None)
    assert r.success is False
    assert "credential" in (r.error or "").lower() or "Missing" in (r.error or "")


def test_bilibili_adapter_upload_success_with_credential():
    from adapter.bilibili_adapter import BilibiliAdapter
    adapter = BilibiliAdapter()
    r = adapter.upload_video("/fake/path", "title", credential={"access_token": "fake"})
    assert r.success is True
    assert r.url is not None


def test_douyin_adapter_interface():
    from adapter.douyin_adapter import DouyinAdapter
    adapter = DouyinAdapter()
    assert adapter.platform_name == "douyin"
    assert adapter.authorize({"access_token": "x"}) is True
    assert adapter.authorize({}) is False


def test_mock_adapter():
    from adapter.mock_adapter import MockAdapter
    adapter = MockAdapter(platform="test")
    assert adapter.platform_name == "test"
    assert adapter.authorize({"cookie": "x"}) is True
    r = adapter.upload_video("/p", "t", credential={"cookie": "x"})
    assert r.success is True
    dr = adapter.fetch_data()
    assert dr.success is True and dr.metrics is not None


def test_xiaohongshu_adapter_use_mock_toggle():
    from adapter.xiaohongshu_adapter import XiaohongshuAdapter
    try:
        from config.platform_config import XiaohongshuConfig
    except ImportError:
        from video_distribution_tool.config.platform_config import XiaohongshuConfig
    config = XiaohongshuConfig(use_mock=True)
    adapter = XiaohongshuAdapter(config=config)
    r = adapter.upload_video("/p", "t", credential={"cookie": "x"})
    assert r.success is True
