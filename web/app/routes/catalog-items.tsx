import type { Route } from "./+types/project";
import { z } from 'zod';
import { Form, redirect, useLoaderData } from "react-router";
import {commitSession, getSession, destroySession} from "~/server"
import Drawer from "../ui/Drawer"
import React, { useState } from "react";
import {isDialogOpen} from '../signals'
import { useSignals } from '@preact/signals-react/runtime';
import { PhotoIcon, UserCircleIcon } from '@heroicons/react/24/solid'
import dotenv from 'dotenv';
import process from "node:process";



export async function action({ request }: Route.ActionArgs) {
  dotenv.config({ path: './../.env' });
  const formData = await request.formData();
  const session = await getSession(request.headers.get('Cookie'));
  const tokens = session.get("tokens")
  const BASE_URL = process.env.API_URL + "/api/equipment/catalog-items/"
  let userApiRes: Response;
  try {
    userApiRes = await fetch(BASE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        'Authorization': 'Bearer ' + tokens.access,
      },
      body: JSON.stringify({
        name: formData.get("name"),
        category: formData.get("category"),
        subcategory: formData.get("subcategory"),
        brand: formData.get("brand"),
        model: formData.get("model"),
        sellable: formData.get("sellable"),
        rentable: formData.get("rentable"),
        isConsumable: formData.get("isConsumable"),
        defaultRate: formData.get("defaultRate"),
        weight: formData.get("weight"),
        power: formData.get("power"),
        dimensions: formData.get("dimensions"),
        upright_only: formData.get("upright_only"),
        image: formData.get("image"),
      })
    })
  } catch (error) {
    console.error("Error while creating user", error);
    return JSON.stringify({ error: "Не удалось создать пользователя. Попробуйте снова позднее." }, { status: 500 });
  }

  return redirect('/');
}

export async function loader({ request }: Route.LoaderArgs) {
  const session = await getSession(request.headers.get("Cookie"));
  if (session.has("user")){
    const apiUrl = process.env.API_URL + '/api/equipment/catalog-items/'
    const tokens = session.get("tokens")
    const apiRes = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + tokens.access,
      },
    })
    if (!apiRes.ok) {
      throw new Error(apiRes.statusText)
    }
    const apiRestJson= await apiRes.json()
    return apiRestJson
  }
  return
}

const CreateItemFormFields = () =>{
  return (
      <>
          <div className="px-4 py-6 sm:p-8">
            <div className="grid max-w-2xl grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
              <div className="sm:col-span-4">
                <label htmlFor="username" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                  Name of item
                </label>
                <div className="mt-2">
                  <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-1 dark:-outline-offset-1 dark:outline-gray-600 dark:focus-within:outline-indigo-500">
                    <input
                      name="name"
                      type="text"
                      placeholder="Kara speacer"
                      className="block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500"
                    />
                  </div>
                </div>
              </div>
              <div className="sm:col-span-4">
                <label htmlFor="username" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                  Category
                </label>
                <div className="mt-2">
                  <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-1 dark:-outline-offset-1 dark:outline-gray-600 dark:focus-within:outline-indigo-500">
                    <input
                      name="category"
                      type="text"
                      placeholder="Sound"
                      className="block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500"
                    />
                  </div>
                </div>
              </div>
              <div className="sm:col-span-4">
                <label htmlFor="username" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                  Subcategory
                </label>
                <div className="mt-2">
                  <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-1 dark:-outline-offset-1 dark:outline-gray-600 dark:focus-within:outline-indigo-500">
                    <input
                      name="subcategory"
                      type="text"
                      placeholder="Speacers"
                      className="block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500"
                    />
                  </div>
                </div>
              </div>
              <div className="sm:col-span-4">
                <label htmlFor="username" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                  Brand
                </label>
                <div className="mt-2">
                  <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-1 dark:-outline-offset-1 dark:outline-gray-600 dark:focus-within:outline-indigo-500">
                    <input
                      name="brand"
                      type="text"
                      placeholder="L'acustic"
                      className="block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500"
                    />
                  </div>
                </div>
              </div>
              <div className="sm:col-span-4">
                <label htmlFor="username" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                  model
                </label>
                <div className="mt-2">
                  <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-1 dark:-outline-offset-1 dark:outline-gray-600 dark:focus-within:outline-indigo-500">
                    <input
                      name="model"
                      type="text"
                      placeholder="Kara"
                      className="block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500"
                    />
                  </div>
                </div>
              </div>
              <div className="sm:col-span-4">
                <label htmlFor="username" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                  defaultRate
                </label>
                <div className="mt-2">
                  <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-1 dark:-outline-offset-1 dark:outline-gray-600 dark:focus-within:outline-indigo-500">
                    <input
                      name="defaultRate"
                      type="number"
                      placeholder="1000"
                      className="block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500"
                    />
                  </div>
                </div>
              </div>
              <div className="sm:col-span-4">
                <label htmlFor="username" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                  pricePolicy
                </label>
                <div className="mt-2">
                  <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-1 dark:-outline-offset-1 dark:outline-gray-600 dark:focus-within:outline-indigo-500">
                    <input
                      name="pricePolicy"
                      type="number"
                      placeholder="1000"
                      className="block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500"
                    />
                  </div>
                </div>
              </div>
              <div className="sm:col-span-4">
                <label htmlFor="weight" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                  Weight
                </label>
                <div className="mt-2">
                  <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-1 dark:-outline-offset-1 dark:outline-gray-600 dark:focus-within:outline-indigo-500">
                    <input
                      id={"weight"}
                      name="weight"
                      type="number"
                      placeholder="1000"
                      className="block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500"
                    />
                  </div>
                </div>
              </div>
              <div className="sm:col-span-4">
                <label htmlFor="weight" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                  power
                </label>
                <div className="mt-2">
                  <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-1 dark:-outline-offset-1 dark:outline-gray-600 dark:focus-within:outline-indigo-500">
                    <input
                      id={"power"}
                      name="power"
                      type="text"
                      placeholder="100W"
                      className="block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500"
                    />
                  </div>
                </div>
              </div>
              <div className="sm:col-span-4">
                <label htmlFor="dimensions" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                  dimensions
                </label>
                <div className="mt-2">
                  <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-1 dark:-outline-offset-1 dark:outline-gray-600 dark:focus-within:outline-indigo-500">
                    <input
                      id={"dimensions"}
                      name="dimensions"
                      type="text"
                      placeholder="l200mm/h300mm/w100mm"
                      className="block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500"
                    />
                  </div>
                </div>
              </div>
              <div className="sm:col-span-4">
                <label htmlFor="upright_only" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                  upright_only
                </label>
                <div className="mt-2">
                  <div className="">
                    <input
                      id={"upright_only"}
                      name="upright_only"
                      type="radio"
                      className="block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500"
                    />
                  </div>
                </div>
              </div>

              <div className="col-span-full">
                <label htmlFor="image" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                  image
                </label>
                <div className="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10 dark:border-white/25">
                  <div className="text-center">
                    <PhotoIcon aria-hidden="true" className="mx-auto size-12 text-gray-300 dark:text-gray-500" />
                    <div className="mt-4 flex text-sm/6 text-gray-600 dark:text-gray-400">
                      <label
                        htmlFor="file-upload"
                        className="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-2 focus-within:outline-offset-2 focus-within:outline-indigo-600 hover:text-indigo-500 dark:bg-transparent dark:text-indigo-400 dark:focus-within:outline-indigo-500 dark:hover:text-indigo-300"
                      >
                        <span>Upload a file</span>
                        <input id="file-upload" name="image" type="file" className="sr-only" />
                      </label>
                      <p className="pl-1">or drag and drop</p>
                    </div>
                    <p className="text-xs/5 text-gray-600 dark:text-gray-400">PNG, JPG, GIF up to 10MB</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
      </>
  )
}

export default function CatalogItems() {
  const loaderdata = useLoaderData()
  const columns = loaderdata && Object.keys(loaderdata[0])
  const [open, setOpen] = useState(false);
  useSignals()

  return (
    <div className="px-4 sm:px-6 lg:px-8">
      <Drawer
          children={<CreateItemFormFields/>}
          method={"POST"}
          action={"/catalog-items"}
      />
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-base font-semibold text-gray-900 dark:text-white">Users</h1>
          <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
            A list of all the users in your account including their name, title, email and role.
          </p>
        </div>
        <div className="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
          <button
            onClick={() => {isDialogOpen.value = true}}
            type="button"
            className="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:bg-indigo-500 dark:hover:bg-indigo-400 dark:focus-visible:outline-indigo-500"
          >
            Add user
          </button>
        </div>
      </div>
      <div className="mt-8 flow-root">

        <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <div className="overflow-hidden shadow-sm outline-1 outline-black/5 sm:rounded-lg dark:shadow-none dark:-outline-offset-1 dark:outline-white/10">

              <table className="relative min-w-full divide-y divide-gray-300 dark:divide-white/15">
                <thead className="bg-gray-50 dark:bg-gray-800/75">
                  <tr>
                    {columns.map((item) => (
                        <th
                          scope="col"
                          className="py-3.5 pr-3 pl-4 text-left text-sm font-semibold text-gray-900 sm:pl-6 dark:text-gray-200"
                        >
                          {item}
                        </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white dark:divide-white/10 dark:bg-gray-800/50">
                  {loaderdata.map((iteam, index: number) => (
                    <tr key={iteam.email}>
                      {columns.map((data) => (
                          <td className="py-4 pr-3 pl-4 text-sm font-medium whitespace-nowrap text-gray-900 sm:pl-6 dark:text-white">
                            {iteam[data]}
                          </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
