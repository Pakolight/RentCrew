import type { Route } from "./+types/catalog-items";

import { useEffect, useMemo, useState } from "react";
import { Form, useActionData, useLoaderData, useNavigation } from "react-router";

type CatalogItem = {
  id: number;
  sku: string;
  name: string;
  category: string;
  subcategory?: string | null;
  brand?: string | null;
  model?: string | null;
  sellable: boolean;
  rentable: boolean;
  isConsumable: boolean;
  defaultRate: number;
  pricePolicy?: number | null;
  weight?: number | null;
  power?: string | null;
  dimensions?: Record<string, unknown> | null;
  upright_only: boolean;
};

type ActionResponse = {
  ok: boolean;
  message: string;
};

const apiUrl = () => import.meta.env.VITE_API_URL ?? process.env.API_URL;

const parseBoolean = (value: FormDataEntryValue | null) => value === "true" || value === "on";

const parseNumber = (value: FormDataEntryValue | null) => {
  const asString = typeof value === "string" ? value : "";
  const parsed = Number(asString);
  return Number.isFinite(parsed) ? parsed : null;
};

export async function loader({ request }: Route.LoaderArgs) {
  const BASE_URL = apiUrl();

  if (!BASE_URL) {
    return { items: [], error: "API_URL is not configured" };
  }

  const cookie = request.headers.get("cookie") ?? "";
  const response = await fetch(`${BASE_URL}/equipment/catalog-items/`, {
    headers: {
      Cookie: cookie,
    },
    credentials: "include",
  });

  if (!response.ok) {
    return { items: [], error: "Не удалось получить список предметов" };
  }

  const items = (await response.json()) as CatalogItem[];
  return { items, error: null };
}

export async function action({ request }: Route.ActionArgs) {
  const BASE_URL = apiUrl();

  if (!BASE_URL) {
    return { ok: false, message: "API_URL is not configured" } satisfies ActionResponse;
  }

  const formData = await request.formData();
  const intent = formData.get("intent");
  const cookie = request.headers.get("cookie") ?? "";
  const model = formData.get("model");

  const payload = {
    name: (formData.get("name") as string | null)?.trim() ?? "",
    category: (formData.get("category") as string | null) ?? "",
    subcategory: (formData.get("subcategory") as string | null) || null,
    brand: (formData.get("brand") as string | null) || null,
    model: typeof model === "string" ? model : null,
    sellable: parseBoolean(formData.get("sellable")),
    rentable: parseBoolean(formData.get("rentable")),
    isConsumable: parseBoolean(formData.get("isConsumable")),
    defaultRate: parseNumber(formData.get("defaultRate")) ?? 0,
    pricePolicy: parseNumber(formData.get("pricePolicy")),
    weight: parseNumber(formData.get("weight")),
    power: (formData.get("power") as string | null) || null,
    dimensions: null,
    upright_only: parseBoolean(formData.get("upright_only")),
  };

  const commonFetchOptions = {
    headers: {
      "Content-Type": "application/json",
      Cookie: cookie,
    },
    credentials: "include" as const,
  };

  try {
    if (intent === "create") {
      const response = await fetch(`${BASE_URL}/equipment/catalog-items/`, {
        method: "POST",
        body: JSON.stringify(payload),
        ...commonFetchOptions,
      });

      if (!response.ok) {
        return { ok: false, message: "Не удалось создать предмет" } satisfies ActionResponse;
      }

      return { ok: true, message: "Item успешно добавлен" } satisfies ActionResponse;
    }

    if (intent === "update") {
      const id = formData.get("id");
      if (!id) {
        return { ok: false, message: "Не указан идентификатор записи" } satisfies ActionResponse;
      }

      const response = await fetch(`${BASE_URL}/equipment/catalog-items/${id}/`, {
        method: "PATCH",
        body: JSON.stringify(payload),
        ...commonFetchOptions,
      });

      if (!response.ok) {
        return { ok: false, message: "Не удалось обновить предмет" } satisfies ActionResponse;
      }

      return { ok: true, message: "Item обновлен" } satisfies ActionResponse;
    }

    if (intent === "delete") {
      const id = formData.get("id");
      if (!id) {
        return { ok: false, message: "Не указан идентификатор записи" } satisfies ActionResponse;
      }

      const response = await fetch(`${BASE_URL}/equipment/catalog-items/${id}/`, {
        method: "DELETE",
        ...commonFetchOptions,
      });

      if (!response.ok) {
        return { ok: false, message: "Не удалось удалить предмет" } satisfies ActionResponse;
      }

      return { ok: true, message: "Item удален" } satisfies ActionResponse;
    }

    return { ok: false, message: "Неизвестное действие" } satisfies ActionResponse;
  } catch (error) {
    console.error("Error while handling catalog item action", error);
    return { ok: false, message: "Ошибка при выполнении запроса" } satisfies ActionResponse;
  }
}

export default function CatalogItems() {
  const { items, error } = useLoaderData<typeof loader>();
  const actionData = useActionData<typeof action>();
  const navigation = useNavigation();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<CatalogItem | null>(null);

  const isSubmitting = useMemo(() => navigation.state === "submitting", [navigation.state]);

  useEffect(() => {
    if (actionData?.ok) {
      setIsModalOpen(false);
      setEditingItem(null);
    }
  }, [actionData]);

  const openCreateModal = () => {
    setEditingItem(null);
    setIsModalOpen(true);
  };

  const openEditModal = (item: CatalogItem) => {
    setEditingItem(item);
    setIsModalOpen(true);
  };

  return (
    <div className="px-4 py-10 sm:px-6 lg:px-8">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-base font-semibold text-gray-900 dark:text-white">Catalog Items</h1>
          <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
            A list of all catalog items, их категории, бренды и тарифы.
          </p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <button
            type="button"
            onClick={openCreateModal}
            className="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:bg-indigo-500 dark:hover:bg-indigo-400 dark:focus-visible:outline-indigo-500"
          >
            Add Items
          </button>
        </div>
      </div>

      {actionData && (
        <div
          className={`mb-4 rounded-md px-4 py-3 text-sm ${
            actionData.ok
              ? "bg-green-50 text-green-800 dark:bg-green-900/20 dark:text-green-200"
              : "bg-red-50 text-red-800 dark:bg-red-900/20 dark:text-red-200"
          }`}
        >
          {actionData.message}
        </div>
      )}

      {error && (
        <div className="mb-4 rounded-md bg-yellow-50 px-4 py-3 text-sm text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-200">
          {error}
        </div>
      )}

      <div className="mt-8 flow-root">
        <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <div className="overflow-hidden shadow-sm outline-1 outline-black/5 sm:rounded-lg dark:shadow-none dark:-outline-offset-1 dark:outline-white/10">
              <table className="relative min-w-full divide-y divide-gray-300 dark:divide-white/15">
                <thead className="bg-gray-50 dark:bg-gray-800/75">
                  <tr>
                    <th
                      scope="col"
                      className="py-3.5 pr-3 pl-4 text-left text-sm font-semibold text-gray-900 sm:pl-6 dark:text-gray-200"
                    >
                      SKU
                    </th>
                    <th
                      scope="col"
                      className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-gray-200"
                    >
                      Name
                    </th>
                    <th
                      scope="col"
                      className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-gray-200"
                    >
                      Category
                    </th>
                    <th
                      scope="col"
                      className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-gray-200"
                    >
                      Brand / Model
                    </th>
                    <th
                      scope="col"
                      className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-gray-200"
                    >
                      Rate
                    </th>
                    <th
                      scope="col"
                      className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-gray-200"
                    >
                      Options
                    </th>
                    <th scope="col" className="py-3.5 pr-4 pl-3 sm:pr-6">
                      <span className="sr-only">Edit</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white dark:divide-white/10 dark:bg-gray-800/50">
                  {items.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/40">
                      <td className="py-4 pr-3 pl-4 text-sm font-medium whitespace-nowrap text-gray-900 sm:pl-6 dark:text-white">
                        {item.sku}
                      </td>
                      <td className="px-3 py-4 text-sm whitespace-nowrap text-gray-500 dark:text-gray-400">{item.name}</td>
                      <td className="px-3 py-4 text-sm whitespace-nowrap text-gray-500 dark:text-gray-400">
                        {item.category}
                        {item.subcategory ? ` / ${item.subcategory}` : ""}
                      </td>
                      <td className="px-3 py-4 text-sm whitespace-nowrap text-gray-500 dark:text-gray-400">
                        {[item.brand, item.model].filter(Boolean).join(" ") || "—"}
                      </td>
                      <td className="px-3 py-4 text-sm whitespace-nowrap text-gray-500 dark:text-gray-400">
                        {item.defaultRate ?? "—"}
                      </td>
                      <td className="px-3 py-4 text-sm whitespace-nowrap text-gray-500 dark:text-gray-400">
                        <div className="flex gap-2">
                          {item.sellable && (
                            <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700 dark:bg-blue-900/20 dark:text-blue-200">
                              Sellable
                            </span>
                          )}
                          {item.rentable && (
                            <span className="rounded-full bg-green-50 px-3 py-1 text-xs font-semibold text-green-700 dark:bg-green-900/20 dark:text-green-200">
                              Rentable
                            </span>
                          )}
                          {item.isConsumable && (
                            <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-700 dark:bg-amber-900/20 dark:text-amber-200">
                              Consumable
                            </span>
                          )}
                        </div>
                      </td>
                      <td className="py-4 pr-4 pl-3 text-right text-sm font-medium whitespace-nowrap sm:pr-6">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            type="button"
                            onClick={() => openEditModal(item)}
                            className="text-indigo-600 hover:text-indigo-900 dark:text-indigo-400 dark:hover:text-indigo-300"
                          >
                            Edit<span className="sr-only">, {item.name}</span>
                          </button>
                          <Form
                            method="post"
                            replace
                            className="inline-flex"
                            onSubmit={(event) => {
                              if (!confirm("Удалить запись?")) {
                                event.preventDefault();
                              }
                            }}
                          >
                            <input type="hidden" name="intent" value="delete" />
                            <input type="hidden" name="id" value={item.id} />
                            <button
                              type="submit"
                              className="text-red-600 hover:text-red-800 dark:text-red-300 dark:hover:text-red-200"
                            >
                              Delete
                            </button>
                          </Form>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 px-4 py-6 backdrop-blur-sm">
          <div className="w-full max-w-3xl rounded-xl bg-white p-6 shadow-xl ring-1 ring-black/10 dark:bg-gray-900 dark:ring-white/10">
            <div className="flex items-start justify-between">
              <div>
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
                  {editingItem ? "Edit item" : "Add a new item"}
                </h2>
                <p className="text-sm text-gray-600 dark:text-gray-300">
                  Укажите данные оборудования. SKU будет сформирован автоматически из названия и модели.
                </p>
              </div>
              <button
                type="button"
                onClick={() => setIsModalOpen(false)}
                className="rounded-md p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 dark:text-gray-300 dark:hover:bg-gray-800"
              >
                ✕
              </button>
            </div>

            <Form method="post" className="mt-6 space-y-6">
              <input type="hidden" name="intent" value={editingItem ? "update" : "create"} />
              {editingItem && <input type="hidden" name="id" value={editingItem.id} />}

              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-white" htmlFor="name">
                    Name
                  </label>
                  <input
                    required
                    id="name"
                    name="name"
                    defaultValue={editingItem?.name}
                    className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-white/10 dark:bg-gray-800 dark:text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-white" htmlFor="category">
                    Category
                  </label>
                  <input
                    required
                    id="category"
                    name="category"
                    defaultValue={editingItem?.category}
                    className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-white/10 dark:bg-gray-800 dark:text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-white" htmlFor="subcategory">
                    Subcategory
                  </label>
                  <input
                    id="subcategory"
                    name="subcategory"
                    defaultValue={editingItem?.subcategory ?? ""}
                    className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-white/10 dark:bg-gray-800 dark:text-white"
                  />
                </div>
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 sm:col-span-1">
                  <div>
                    <label className="block text-sm font-medium text-gray-900 dark:text-white" htmlFor="brand">
                      Brand
                    </label>
                    <input
                      id="brand"
                      name="brand"
                      defaultValue={editingItem?.brand ?? ""}
                      className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-white/10 dark:bg-gray-800 dark:text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-900 dark:text-white" htmlFor="model">
                      Model
                    </label>
                    <input
                      id="model"
                      name="model"
                      defaultValue={editingItem?.model ?? ""}
                      className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-white/10 dark:bg-gray-800 dark:text-white"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-white" htmlFor="defaultRate">
                    Default rate
                  </label>
                  <input
                    id="defaultRate"
                    name="defaultRate"
                    type="number"
                    step="0.01"
                    defaultValue={editingItem?.defaultRate ?? "0"}
                    className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-white/10 dark:bg-gray-800 dark:text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-white" htmlFor="pricePolicy">
                    Price policy ID
                  </label>
                  <input
                    id="pricePolicy"
                    name="pricePolicy"
                    type="number"
                    defaultValue={editingItem?.pricePolicy ?? ""}
                    className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-white/10 dark:bg-gray-800 dark:text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-white" htmlFor="weight">
                    Weight
                  </label>
                  <input
                    id="weight"
                    name="weight"
                    defaultValue={editingItem?.weight ?? ""}
                    className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-white/10 dark:bg-gray-800 dark:text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-900 dark:text-white" htmlFor="power">
                    Power
                  </label>
                  <input
                    id="power"
                    name="power"
                    defaultValue={editingItem?.power ?? ""}
                    className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 dark:border-white/10 dark:bg-gray-800 dark:text-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                <label className="flex items-center gap-3 text-sm font-medium text-gray-900 dark:text-white">
                  <input
                    type="checkbox"
                    name="sellable"
                    defaultChecked={editingItem?.sellable}
                    className="size-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 dark:border-white/10 dark:bg-gray-800"
                  />
                  Sellable
                </label>
                <label className="flex items-center gap-3 text-sm font-medium text-gray-900 dark:text-white">
                  <input
                    type="checkbox"
                    name="rentable"
                    defaultChecked={editingItem?.rentable ?? true}
                    className="size-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 dark:border-white/10 dark:bg-gray-800"
                  />
                  Rentable
                </label>
                <label className="flex items-center gap-3 text-sm font-medium text-gray-900 dark:text-white">
                  <input
                    type="checkbox"
                    name="isConsumable"
                    defaultChecked={editingItem?.isConsumable}
                    className="size-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 dark:border-white/10 dark:bg-gray-800"
                  />
                  Consumable
                </label>
                <label className="flex items-center gap-3 text-sm font-medium text-gray-900 dark:text-white">
                  <input
                    type="checkbox"
                    name="upright_only"
                    defaultChecked={editingItem?.upright_only}
                    className="size-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 dark:border-white/10 dark:bg-gray-800"
                  />
                  Upright only
                </label>
              </div>

              <div className="flex justify-end gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="rounded-md border border-gray-300 px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 dark:border-white/10 dark:text-gray-100 dark:hover:bg-gray-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-70 dark:bg-indigo-500 dark:hover:bg-indigo-400"
                >
                  {isSubmitting ? "Saving..." : editingItem ? "Update" : "Create"}
                </button>
              </div>
            </Form>
          </div>
        </div>
      )}
    </div>
  );
}
