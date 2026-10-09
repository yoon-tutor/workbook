"""Authoring helpers for producing canonical workbooks without semantic rewrites."""

from .packet import AuthoringPacketError, compact_canonical, expand_packet, verify_new_packet_policy

__all__ = ["AuthoringPacketError", "compact_canonical", "expand_packet", "verify_new_packet_policy"]
