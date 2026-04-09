"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import type { LLMConfig, LLMProvider } from "@/types";
import { useI18n } from "@/lib/i18n";
import { Eye, EyeOff } from "lucide-react";

export default function SettingsPage() {
  const { t } = useI18n();
  const [configs, setConfigs] = useState<LLMConfig[]>([]);
  const [providers, setProviders] = useState<LLMProvider[]>([]);
  const [selectedProvider, setSelectedProvider] = useState("");
  const [selectedModel, setSelectedModel] = useState("");
  const [apiKey, setApiKey] = useState("");
  const [baseUrl, setBaseUrl] = useState("");
  const [isDefault, setIsDefault] = useState(true);
  const [isAdding, setIsAdding] = useState(false);
  const [editingConfig, setEditingConfig] = useState<LLMConfig | null>(null);
  const [editProvider, setEditProvider] = useState("");
  const [editModel, setEditModel] = useState("");
  const [editApiKey, setEditApiKey] = useState("");
  const [editBaseUrl, setEditBaseUrl] = useState("");
  const [editIsDefault, setEditIsDefault] = useState(false);
  const [isUpdating, setIsUpdating] = useState(false);
  const [addApiKeyVisible, setAddApiKeyVisible] = useState(false);
  const [editApiKeyVisible, setEditApiKeyVisible] = useState(false);

  const fetchConfigs = async () => {
    const res = await api.get<LLMConfig[]>("/llm/configs");
    setConfigs(res.data);
  };

  const fetchProviders = async () => {
    const res = await api.get<LLMProvider[]>("/llm/providers");
    setProviders(res.data);
  };

  useEffect(() => {
    fetchConfigs();
    fetchProviders();
  }, []);

  const currentProvider = providers.find((p) => p.id === selectedProvider);

  const handleAdd = async () => {
    if (!selectedProvider || !selectedModel || !apiKey) {
      toast.error(t("settings.fillAll"));
      return;
    }
    if (currentProvider?.requires_base_url && !baseUrl) {
      toast.error(t("settings.baseUrlRequired"));
      return;
    }
    setIsAdding(true);
    try {
      await api.post("/llm/configs", {
        provider: selectedProvider,
        model: selectedModel,
        api_key: apiKey,
        base_url: baseUrl || null,
        is_default: isDefault,
      });
      toast.success(t("settings.configAdded"));
      setApiKey("");
      setBaseUrl("");
      setSelectedProvider("");
      setSelectedModel("");
      fetchConfigs();
    } catch {
      toast.error(t("settings.addFailed"));
    } finally {
      setIsAdding(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/llm/configs/${id}`);
      toast.success(t("settings.configRemoved"));
      fetchConfigs();
    } catch {
      toast.error(t("settings.removeFailed"));
    }
  };

  const handleToggleDefault = async (config: LLMConfig) => {
    const newIsDefault = !config.is_default;
    try {
      await api.put(`/llm/configs/${config.id}`, {
        is_default: newIsDefault,
      });
      toast.success(newIsDefault ? t("settings.setDefaultSuccess") : t("settings.unsetDefaultSuccess"));
      fetchConfigs();
    } catch {
      toast.error(t("settings.updateFailed"));
    }
  };

  const handleEdit = (config: LLMConfig) => {
    setEditingConfig(config);
    setEditProvider(config.provider);
    setEditModel(config.model);
    setEditBaseUrl(config.base_url || "");
    setEditIsDefault(config.is_default);
    setEditApiKey(config.api_key_decrypted || "");
  };

  const handleUpdate = async () => {
    if (!editingConfig) return;
    if (!editProvider || !editModel) {
      toast.error(t("settings.fillAll"));
      return;
    }
    const currentProvider = providers.find((p) => p.id === editProvider);
    if (currentProvider?.requires_base_url && !editBaseUrl) {
      toast.error(t("settings.baseUrlRequired"));
      return;
    }
    setIsUpdating(true);
    try {
      const updateData: Record<string, unknown> = {};
      if (editProvider !== editingConfig.provider) updateData.provider = editProvider;
      if (editModel !== editingConfig.model) updateData.model = editModel;
      if (editBaseUrl !== (editingConfig.base_url || "")) updateData.base_url = editBaseUrl || null;
      if (editApiKey && editApiKey !== editingConfig.api_key_decrypted) updateData.api_key = editApiKey;
      if (editIsDefault !== editingConfig.is_default) updateData.is_default = editIsDefault;

      await api.put(`/llm/configs/${editingConfig.id}`, updateData);
      toast.success(t("settings.configUpdated"));
      setEditingConfig(null);
      setEditApiKey("");
      fetchConfigs();
    } catch {
      toast.error(t("settings.updateFailed"));
    } finally {
      setIsUpdating(false);
    }
  };

  const handleCancelEdit = () => {
    setEditingConfig(null);
    setEditApiKey("");
  };

  return (
    <div className="p-6 max-w-2xl space-y-6">
      <h2 className="text-2xl font-bold">{t("settings.title")}</h2>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">{t("settings.llmConfig")}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>{t("settings.provider")}</Label>
            <Select value={selectedProvider} onValueChange={(v) => {
              if (v) {
                setSelectedProvider(v);
                const prov = providers.find((p) => p.id === v);
                if (prov?.requires_base_url) {
                  setSelectedModel(prov.models[0] || "default");
                } else {
                  setSelectedModel("");
                }
                setBaseUrl("");
              }
            }}>
              <SelectTrigger><SelectValue placeholder={t("settings.selectProvider")} /></SelectTrigger>
              <SelectContent>
                {providers.map((p) => (
                  <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {currentProvider && (
            <>
              {!currentProvider.requires_base_url && (
                <div className="space-y-2">
                  <Label>{t("settings.model")}</Label>
                  <Select value={selectedModel} onValueChange={(v) => { if (v) setSelectedModel(v); }}>
                    <SelectTrigger><SelectValue placeholder={t("settings.selectModel")} /></SelectTrigger>
                    <SelectContent>
                      {currentProvider.models.map((m) => (
                        <SelectItem key={m} value={m}>{m}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              )}

              {currentProvider.requires_base_url ? (
                <div className="space-y-4 rounded-md border p-4 bg-muted/20">
                  <p className="text-xs font-medium text-muted-foreground">
                    {currentProvider.name} {t("settings.connection")}
                  </p>
                  <div className="space-y-2">
                    <Label>{t("settings.baseUrl")} <span className="text-destructive">*</span></Label>
                    <Input
                      type="url"
                      placeholder={t("settings.baseUrlPlaceholder")}
                      value={baseUrl}
                      onChange={(e) => setBaseUrl(e.target.value)}
                    />
                    <p className="text-[11px] text-muted-foreground">
                      {t("settings.baseUrlHint")}
                    </p>
                  </div>
                  <div className="space-y-2">
                    <Label>{t("settings.apiKey")} <span className="text-destructive">*</span></Label>
                    <div className="relative">
                      <Input
                        type={addApiKeyVisible ? "text" : "password"}
                        placeholder={t("settings.difyApiKeyPlaceholder")}
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                        className="pr-10"
                        autoComplete="new-password"
                        data-1p-ignore
                      />
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                        onClick={() => setAddApiKeyVisible(!addApiKeyVisible)}
                        title={addApiKeyVisible ? t("settings.hideApiKey") : t("settings.showApiKey")}
                      >
                        {addApiKeyVisible ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </Button>
                    </div>
                    <p className="text-[11px] text-muted-foreground">
                      {t("settings.difyApiKey")}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="space-y-2">
                  <Label>{t("settings.apiKey")}</Label>
                  <div className="relative">
                    <Input
                      type={addApiKeyVisible ? "text" : "password"}
                      placeholder={t("settings.apiKeyPlaceholder")}
                      value={apiKey}
                      onChange={(e) => setApiKey(e.target.value)}
                      className="pr-10"
                      autoComplete="new-password"
                      data-1p-ignore
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                      onClick={() => setAddApiKeyVisible(!addApiKeyVisible)}
                      title={addApiKeyVisible ? t("settings.hideApiKey") : t("settings.showApiKey")}
                    >
                      {addApiKeyVisible ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>
              )}
            </>
          )}

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="isDefault"
              checked={isDefault}
              onChange={(e) => setIsDefault(e.target.checked)}
            />
            <Label htmlFor="isDefault">{t("settings.setDefault")}</Label>
          </div>

          <Button onClick={handleAdd} disabled={isAdding}>
            {isAdding ? t("settings.adding") : t("settings.addConfig")}
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">{t("settings.savedConfigs")}</CardTitle>
        </CardHeader>
        <CardContent>
          {configs.length === 0 ? (
            <p className="text-sm text-muted-foreground">{t("settings.noConfigs")}</p>
          ) : (
            <div className="space-y-3">
              {configs.map((config) => {
                const providerInfo = providers.find((p) => p.id === config.provider);
                const displayName = providerInfo?.name || config.provider;
                const isEditing = editingConfig?.id === config.id;

                if (isEditing) {
                  return (
                    <div key={config.id} className="border rounded-md p-4 space-y-3">
                      <div className="space-y-2">
                        <Label>{t("settings.provider")}</Label>
                        <Select value={editProvider} onValueChange={(v) => {
                          setEditProvider(v);
                          const prov = providers.find((p) => p.id === v);
                          if (prov?.requires_base_url) {
                            setEditModel(prov.models[0] || "default");
                          } else {
                            setEditModel("");
                          }
                          setEditBaseUrl("");
                        }}>
                          <SelectTrigger><SelectValue /></SelectTrigger>
                          <SelectContent>
                            {providers.map((p) => (
                              <SelectItem key={p.id} value={p.id}>{p.name}</SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>

                      {editProvider && !providers.find((p) => p.id === editProvider)?.requires_base_url && (
                        <div className="space-y-2">
                          <Label>{t("settings.model")}</Label>
                          <Select value={editModel} onValueChange={(v) => setEditModel(v)}>
                            <SelectTrigger><SelectValue /></SelectTrigger>
                            <SelectContent>
                              {providers.find((p) => p.id === editProvider)?.models.map((m) => (
                                <SelectItem key={m} value={m}>{m}</SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                      )}

                      {providers.find((p) => p.id === editProvider)?.requires_base_url && (
                        <div className="space-y-2">
                          <Label>{t("settings.baseUrl")}</Label>
                          <Input
                            type="url"
                            placeholder={t("settings.baseUrlPlaceholder")}
                            value={editBaseUrl}
                            onChange={(e) => setEditBaseUrl(e.target.value)}
                          />
                        </div>
                      )}

                      <div className="space-y-2">
                        <Label>{t("settings.apiKey")}</Label>
                        <div className="relative">
                          <Input
                            type={editApiKeyVisible ? "text" : "password"}
                            placeholder={t("settings.apiKeyPlaceholder")}
                            value={editApiKey}
                            onChange={(e) => setEditApiKey(e.target.value)}
                            className="pr-10"
                            autoComplete="new-password"
                            data-1p-ignore
                          />
                          <Button
                            type="button"
                            variant="ghost"
                            size="sm"
                            className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                            onClick={() => setEditApiKeyVisible(!editApiKeyVisible)}
                            title={editApiKeyVisible ? t("settings.hideApiKey") : t("settings.showApiKey")}
                          >
                            {editApiKeyVisible ? (
                              <EyeOff className="h-4 w-4" />
                            ) : (
                              <Eye className="h-4 w-4" />
                            )}
                          </Button>
                        </div>
                        <p className="text-[11px] text-muted-foreground">
                          {t("settings.leaveBlankToKeep")}
                        </p>
                      </div>

                      <div className="flex items-center gap-2">
                        <input
                          type="checkbox"
                          id={`editDefault-${config.id}`}
                          checked={editIsDefault}
                          onChange={(e) => setEditIsDefault(e.target.checked)}
                        />
                        <Label htmlFor={`editDefault-${config.id}`}>{t("settings.setDefault")}</Label>
                      </div>

                      <div className="flex gap-2">
                        <Button onClick={handleUpdate} disabled={isUpdating} size="sm">
                          {t("common.save")}
                        </Button>
                        <Button variant="outline" onClick={handleCancelEdit} size="sm">
                          {t("common.cancel")}
                        </Button>
                      </div>
                    </div>
                  );
                }

                return (
                  <div key={config.id} className="border rounded-md p-3">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium">{displayName}</span>
                        {!config.base_url && (
                          <span className="text-sm text-muted-foreground">{config.model}</span>
                        )}
                        {config.is_default && <Badge>{t("common.default")}</Badge>}
                      </div>
                      <div className="flex gap-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleToggleDefault(config)}
                          title={config.is_default ? t("settings.unsetDefault") : t("settings.setDefault")}
                        >
                          {config.is_default ? t("settings.unsetDefaultIcon") : t("settings.setDefaultIcon")}
                        </Button>
                        <Button variant="ghost" size="sm" onClick={() => handleEdit(config)}>
                          {t("common.edit")}
                        </Button>
                        <Button variant="ghost" size="sm" onClick={() => handleDelete(config.id)}>
                          {t("common.remove")}
                        </Button>
                      </div>
                    </div>
                    <div className="space-y-0.5">
                      {config.base_url ? (
                        <>
                          <p className="text-xs text-muted-foreground">URL: {config.base_url}</p>
                          <p className="text-xs text-muted-foreground">Key: {config.api_key_hint}</p>
                        </>
                      ) : (
                        <p className="text-xs text-muted-foreground">Key: {config.api_key_hint}</p>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
