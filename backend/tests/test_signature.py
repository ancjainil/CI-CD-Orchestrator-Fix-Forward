import hashlib
import hmac

from app.services.github_client import verify_signature


def test_verify_signature_ok():
    body = b'{"hello":"world"}'
    secret = "topsecret"
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    sig = f"sha256={digest}"
    assert verify_signature(body, sig, secret)


def test_verify_signature_fail():
    body = b'{}'
    assert not verify_signature(body, "sha256=deadbeef", "secret")
