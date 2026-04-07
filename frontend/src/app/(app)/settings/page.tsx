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
                    <Input
                      type="password"
                      placeholder={t("settings.difyApiKeyPlaceholder")}
                      value={apiKey}
                      onChange={(e) => setApiKey(e.target.value)}
                    />
                    <p className="text-[11px] text-muted-foreground">
                      {t("settings.difyApiKey")}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="space-y-2">
                  <Label>{t("settings.apiKey")}</Label>
                  <Input
                    type="password"
                    placeholder={t("settings.apiKeyPlaceholder")}
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                  />
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
            <div className="space-y-2">
              {configs.map((config) => {
                const providerInfo = providers.find((p) => p.id === config.provider);
                const displayName = providerInfo?.name || config.provider;
                return (
                  <div key={config.id} className="flex items-center justify-between border rounded-md p-3">
                    <div className="space-y-0.5">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium">{displayName}</span>
                        {!config.base_url && (
                          <span className="text-sm text-muted-foreground">{config.model}</span>
                        )}
                        {config.is_default && <Badge>{t("common.default")}</Badge>}
                      </div>
                      {config.base_url ? (
                        <>
                          <p className="text-xs text-muted-foreground">URL: {config.base_url}</p>
                          <p className="text-xs text-muted-foreground">Key: {config.api_key_hint}</p>
                        </>
                      ) : (
                        <p className="text-xs text-muted-foreground">Key: {config.api_key_hint}</p>
                      )}
                    </div>
                    <Button variant="ghost" size="sm" onClick={() => handleDelete(config.id)}>
                      {t("common.remove")}
                    </Button>
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
