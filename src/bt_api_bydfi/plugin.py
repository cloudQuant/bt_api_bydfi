"""Module-level docstring."""
# generated, verify register call

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from bt_api_base.plugins.protocol import PluginInfo

from bt_api_bydfi.registry_registration import register_bydfi

if TYPE_CHECKING:
    from bt_api_base.registry import ExchangeRegistry


def register_plugin(registry: ExchangeRegistry, runtime_factory: Any) -> PluginInfo:
    """register_plugin function"""
    register_bydfi()

    return PluginInfo(
        name="bt_api_bydfi",
        version="0.1.0",
        core_requires=">=0.15,<1.0",
        supported_exchanges=("BYDFI___SPOT",),
        supported_asset_types=("SPOT",),
    )
