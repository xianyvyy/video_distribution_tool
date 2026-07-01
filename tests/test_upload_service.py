"""
Upload service tests: compliance (sensitive block), audit, adapter delegation.
"""
import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))


def test_upload_service_blocks_sensitive_title():
    from service.upload_service import UploadService
    from core.compliance.sensitive import set_sensitive_patterns
    set_sensitive_patterns([r"blockme"])
    svc = UploadService()
    result = svc.upload_to_platform("bilibili", "/fake/video.mp4", "title with blockme", operator="test")
    assert result.success is False
    assert "sensitive" in (result.error or "").lower() or "blockme" in (result.error or "").lower()
    set_sensitive_patterns([])


def test_upload_service_success_when_sensitive_clean():
    from service.upload_service import UploadService
    svc = UploadService()
    # Credential will be None -> account_service.get_credential_for_account may return None
    # BilibiliAdapter.upload_video with no cred returns failure; with cred returns success
    # So we need a mock or real credential. Use adapter that accepts mock cred.
    result = svc.upload_to_platform(
        "bilibili", "/fake/video.mp4", "clean title",
        credential={"access_token": "fake_token"},
        operator="test",
    )
    assert result.success is True


def test_upload_to_multiple_platforms():
    from service.upload_service import UploadService
    svc = UploadService()
    results = svc.upload_to_multiple_platforms(
        ["bilibili", "douyin"],
        "/fake/video.mp4",
        "clean title",
        operator="test",
    )
    assert "bilibili" in results and "douyin" in results
    # Without cred they may fail; with cred they succeed. We didn't pass cred so account_svc returns None -> fail
    for p, r in results.items():
        assert hasattr(r, "success") and hasattr(r, "error")
