"""
ORM models: account, upload task, video record, etc.
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(String(32), nullable=False, index=True)
    name = Column(String(255), nullable=True)
    # Encrypted credential blob (from core/encryption)
    credential_encrypted = Column(Text, nullable=True)
    extra_meta = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UploadTask(Base):
    __tablename__ = "upload_tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    platform = Column(String(32), nullable=False, index=True)
    video_path = Column(String(1024), nullable=True)
    title = Column(String(512), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(32), default="pending")  # pending, uploading, done, failed
    result_url = Column(String(1024), nullable=True)
    error_message = Column(Text, nullable=True)
    # For resumable upload: store uploaded chunk keys or offset
    resume_meta = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DataSnapshot(Base):
    __tablename__ = "data_snapshots"
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    platform = Column(String(32), nullable=False, index=True)
    snapshot_at = Column(DateTime, default=datetime.utcnow)
    metrics = Column(JSON, nullable=True)  # play_count, like_count, etc.
