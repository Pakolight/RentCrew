import type { Route } from "./+types/project";

import { PhotoIcon, UserCircleIcon } from '@heroicons/react/24/solid'
import { ChevronDownIcon } from '@heroicons/react/16/solid'
import { Form, redirect, useSubmit } from 'react-router'
import * as process from "node:process";
import * as crypto from 'crypto';
import dotenv from 'dotenv';
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

// Define validation schema using zod
const registrationSchema = z.object({
  first_name: z.string().min(2, { message: "First name must be at least 2 characters" }),
  last_name: z.string().min(2, { message: "Last name must be at least 2 characters" }),
  email: z.string().email({ message: "Invalid email address" }),
  legalName: z.string().min(2, { message: "Company name must be at least 2 characters" }),
  tradeName: z.string().min(2, { message: "Trade name must be at least 2 characters" }),
  vatNumber: z.string().min(3, { message: "VAT number must be at least 3 characters" }),
  iban: z.string().min(5, { message: "IBAN must be at least 5 characters" }),
  country: z.string().min(1, { message: "Country is required" }),
  street_address: z.string().min(3, { message: "Street address must be at least 3 characters" }),
  city: z.string().min(2, { message: "City must be at least 2 characters" }),
  state_province: z.string().min(2, { message: "State/Province must be at least 2 characters" }),
  zip_postal_code: z.string().min(3, { message: "ZIP/Postal code must be at least 3 characters" })
});

// Type for our form data
type RegistrationFormData = z.infer<typeof registrationSchema>;

export async function action({request,}: Route.ActionArgs) {
  const formData = await request.formData()
  dotenv.config({ path: './../.env' });

  function generatePassword(length = 8) {
    const buffer = crypto.randomBytes(length);
    return buffer.toString('base64').replace(/[+/=]/g, '').slice(0, length);
  }

  const BASE_URL = process.env.API_URL
  const userApiRes = await fetch( `${BASE_URL}/api/auth/create/user/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: formData.get("email"),
      first_name: formData.get("first_name"),
      last_name: formData.get("last_name"),
      role: 'user',
      password: generatePassword(),
    })
  })

  let userApiResJson: unknown = null;
  const text = await userApiRes.text();
  try { userApiResJson = text ? JSON.parse(text) : null; } catch { userApiResJson = text; }

  const companyApiRes = await fetch( `${BASE_URL}/api/auth/create/company/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      "owner":
          `${userApiResJson["id"]}`
      ,
      "legalName":
          formData.get("legalName")
      ,
      "tradeName":
          formData.get("tradeName")
      ,
      "vatNumber":
          formData.get("vatNumber")
      ,
      "iban":
          formData.get("iban")
      ,
      "country":
          formData.get("country")
      ,
      "street_address":
          formData.get("street_address")
      ,
      "city":
        formData.get("city")
      ,
      "state_province":
        formData.get("state_province")
      ,
      "zip_postal_code":
        formData.get("zip_postal_code")

    })
  })


  return redirect('/login')
}


export default function Registration() {
  const submit = useSubmit();
  const {
    register, 
    handleSubmit, 
    formState: { errors, isSubmitting, isDirty, isValid }
  } = useForm<RegistrationFormData>({
    resolver: zodResolver(registrationSchema),
    mode: "onBlur"
  });

  // Function to handle form submission
  const onSubmit = (data: RegistrationFormData) => {
    console.log("Form submitted successfully:", data);
    // Form is valid, proceed with submission

    // Create FormData and append all fields
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
      formData.append(key, value);
    });

    // Submit the form data to the action function
    submit(formData, { method: "POST" });
  };

  // Get all error messages for display in the summary
  const errorMessages = Object.entries(errors).map(([field, error]) => ({
    field,
    message: error?.message as string
  }));

  return (
    <Form method="post" onSubmit={handleSubmit(onSubmit)}>
      {/* Error Summary */}
      {errorMessages.length > 0 && (
        <div className="mb-6 p-4 border border-red-300 rounded-md bg-red-50 dark:bg-red-900/10 dark:border-red-900/30">
          <h3 className="text-sm font-medium text-red-800 dark:text-red-400">Please fix the following errors:</h3>
          <ul className="mt-2 text-sm text-red-700 dark:text-red-500 list-disc list-inside">
            {errorMessages.map(({ field, message }) => (
              <li key={field}>{message}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="space-y-12">
        {/* Personal users Information section */}
        <div className="grid grid-cols-1 gap-x-8 gap-y-10 border-b border-gray-900/10 pb-12 md:grid-cols-3 dark:border-white/10">
          <div>
            <h2 className="text-base/7 font-semibold text-gray-900 dark:text-white">Personal Information</h2>
            <p className="mt-1 text-sm/6 text-gray-600 dark:text-gray-400">
              Заполните здесь данные владельца компании, эти данные буду использоваться для входа
            </p>
          </div>

          <div className="grid max-w-2xl grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6 md:col-span-2">
            <div className="sm:col-span-3">
              <label htmlFor="first-name" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                First name
              </label>
              <div className="mt-2">
                <input
                  id="first_name"
                  {...register("first_name")}
                  type="text"
                  autoComplete="given-name"
                  className={`block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 ${errors.first_name ? 'outline-red-500' : 'outline-gray-300'} placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:placeholder:text-gray-500 dark:focus:outline-indigo-500`}
                />
                {errors.first_name && (
                  <p className="mt-1 text-sm text-red-600">{errors.first_name.message}</p>
                )}
              </div>
            </div>
            <div className="sm:col-span-3">
              <label htmlFor="last-name" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                Last name
              </label>
              <div className="mt-2">
                <input
                  id="last_name"
                  {...register("last_name")}
                  type="text"
                  autoComplete="family-name"
                  className={`block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 ${errors.last_name ? 'outline-red-500' : 'outline-gray-300'} placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:placeholder:text-gray-500 dark:focus:outline-indigo-500`}
                />
                {errors.last_name && (
                  <p className="mt-1 text-sm text-red-600">{errors.last_name.message}</p>
                )}
              </div>
            </div>


            <div className="sm:col-span-4">
              <label htmlFor="email" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                Email address
              </label>
              <div className="mt-2">
                <input
                  id="email"
                  {...register("email")}
                  type="email"
                  autoComplete="email"
                  className={`block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 ${errors.email ? 'outline-red-500' : 'outline-gray-300'} placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:placeholder:text-gray-500 dark:focus:outline-indigo-500`}
                />
                {errors.email && (
                  <p className="mt-1 text-sm text-red-600">{errors.email.message}</p>
                )}
              </div>
            </div>
            <div className="col-span-full">
              <label htmlFor="photo" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                Avatar
              </label>
              <div className="mt-2 flex items-center gap-x-3">
                <UserCircleIcon aria-hidden="true" className="size-12 text-gray-300 dark:text-gray-500" />
                <button
                  type="button"
                  className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs inset-ring inset-ring-gray-300 hover:bg-gray-50 dark:bg-white/10 dark:text-white dark:shadow-none dark:inset-ring-white/5 dark:hover:bg-white/20"
                >
                  Change
                </button>
              </div>
            </div>

          </div>
        </div>

        <div className="grid grid-cols-1 gap-x-8 gap-y-10 border-b border-gray-900/10 pb-12 md:grid-cols-3 dark:border-white/10">
          <div>
            <h2 className="text-base/7 font-semibold text-gray-900 dark:text-white">Company profile</h2>
            <p className="mt-1 text-sm/6 text-gray-600 dark:text-gray-400">
              Заполните данные своей компании
            </p>
          </div>

          <div className="grid max-w-2xl grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6 md:col-span-2">
            <div className="sm:col-span-4">
              <label htmlFor="username" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                Company name
              </label>
              <div className="mt-2">
                <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-white/10 dark:focus-within:outline-indigo-500">
                  <div className="shrink-0 text-base text-gray-500 select-none sm:text-sm/6 dark:text-gray-400">

                  </div>
                  <input
                    id="legalName"
                    {...register("legalName")}
                    type="text"
                    placeholder="RentCrew"
                    className={`block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500 ${errors.legalName ? 'border-red-500' : ''}`}
                  />
                  {errors.legalName && (
                    <p className="mt-1 text-sm text-red-600">{errors.legalName.message}</p>
                  )}
                </div>
              </div>
            </div>
            <div className="sm:col-span-4">
              <label htmlFor="username" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                Trade name
              </label>
              <div className="mt-2">
                <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-white/10 dark:focus-within:outline-indigo-500">
                  <div className="shrink-0 text-base text-gray-500 select-none sm:text-sm/6 dark:text-gray-400">

                  </div>
                  <input
                    id="tradeName"
                    {...register("tradeName")}
                    type="text"
                    placeholder="Rent crew audio-vizual BV"
                    className={`block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500 ${errors.tradeName ? 'border-red-500' : ''}`}
                  />
                  {errors.tradeName && (
                    <p className="mt-1 text-sm text-red-600">{errors.tradeName.message}</p>
                  )}
                </div>
              </div>
            </div>
            <div className="sm:col-span-4">
              <label htmlFor="username" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                Vat number
              </label>
              <div className="mt-2">
                <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-white/10 dark:focus-within:outline-indigo-500">
                  <div className="shrink-0 text-base text-gray-500 select-none sm:text-sm/6 dark:text-gray-400">

                  </div>
                  <input
                    id="vatNumber"
                    {...register("vatNumber")}
                    type="text"
                    placeholder="BV123456 SN"
                    className={`block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500 ${errors.vatNumber ? 'border-red-500' : ''}`}
                  />
                  {errors.vatNumber && (
                    <p className="mt-1 text-sm text-red-600">{errors.vatNumber.message}</p>
                  )}
                </div>
              </div>
            </div>
            <div className="sm:col-span-4">
              <label htmlFor="username" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                iban
              </label>
              <div className="mt-2">
                <div className="flex items-center rounded-md bg-white pl-3 outline-1 -outline-offset-1 outline-gray-300 focus-within:outline-2 focus-within:-outline-offset-2 focus-within:outline-indigo-600 dark:bg-white/5 dark:outline-white/10 dark:focus-within:outline-indigo-500">
                  <div className="shrink-0 text-base text-gray-500 select-none sm:text-sm/6 dark:text-gray-400">

                  </div>
                  <input
                    id="iban"
                    {...register("iban")}
                    type="text"
                    placeholder="1234567BJ"
                    className={`block min-w-0 grow bg-white py-1.5 pr-3 pl-1 text-base text-gray-900 placeholder:text-gray-400 focus:outline-none sm:text-sm/6 dark:bg-transparent dark:text-white dark:placeholder:text-gray-500 ${errors.iban ? 'border-red-500' : ''}`}
                  />
                  {errors.iban && (
                    <p className="mt-1 text-sm text-red-600">{errors.iban.message}</p>
                  )}
                </div>
              </div>
            </div>
            <div className="col-span-full">
              <label htmlFor="photo" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                Logo
              </label>
              <div className="mt-2 flex items-center gap-x-3">
                <UserCircleIcon aria-hidden="true" className="size-12 text-gray-300 dark:text-gray-500" />
                <button
                  type="button"
                  className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs inset-ring inset-ring-gray-300 hover:bg-gray-50 dark:bg-white/10 dark:text-white dark:shadow-none dark:inset-ring-white/5 dark:hover:bg-white/20"
                >
                  Change
                </button>
              </div>
            </div>
            <div className="sm:col-span-3">
              <label htmlFor="country" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                Country
              </label>
              <div className="mt-2 grid grid-cols-1">
                <select
                  id="country"
                  {...register("country")}
                  autoComplete="country-name"
                  className={`col-start-1 row-start-1 w-full appearance-none rounded-md bg-white py-1.5 pr-8 pl-3 text-base text-gray-900 outline-1 -outline-offset-1 ${errors.country ? 'outline-red-500' : 'outline-gray-300'} focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:*:bg-gray-800 dark:focus:outline-indigo-500`}
                >
                  <option value="">Select a country</option>
                  <option value="United States">United States</option>
                  <option value="Canada">Canada</option>
                  <option value="Mexico">Mexico</option>
                </select>
                {errors.country && (
                  <p className="mt-1 text-sm text-red-600">{errors.country.message}</p>
                )}
                <ChevronDownIcon
                  aria-hidden="true"
                  className="pointer-events-none col-start-1 row-start-1 mr-2 size-5 self-center justify-self-end text-gray-500 sm:size-4 dark:text-gray-400"
                />
              </div>
            </div>
            <div className="col-span-full">
              <label htmlFor="street-address" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                Street address
              </label>
              <div className="mt-2">
                <input
                  id="street_address"
                  {...register("street_address")}
                  type="text"
                  autoComplete="street-address"
                  className={`block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 ${errors.street_address ? 'outline-red-500' : 'outline-gray-300'} placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:placeholder:text-gray-500 dark:focus:outline-indigo-500`}
                />
                {errors.street_address && (
                  <p className="mt-1 text-sm text-red-600">{errors.street_address.message}</p>
                )}
              </div>
            </div>
            <div className="sm:col-span-2 sm:col-start-1">
              <label htmlFor="city" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                City
              </label>
              <div className="mt-2">
                <input
                  id="city"
                  {...register("city")}
                  type="text"
                  autoComplete="address-level2"
                  className={`block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 ${errors.city ? 'outline-red-500' : 'outline-gray-300'} placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:placeholder:text-gray-500 dark:focus:outline-indigo-500`}
                />
                {errors.city && (
                  <p className="mt-1 text-sm text-red-600">{errors.city.message}</p>
                )}
              </div>
            </div>
            <div className="sm:col-span-2">
              <label htmlFor="region" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                State / Province
              </label>
              <div className="mt-2">
                <input
                  id="state_province"
                  {...register("state_province")}
                  type="text"
                  autoComplete="address-level1"
                  className={`block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 ${errors.state_province ? 'outline-red-500' : 'outline-gray-300'} placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:placeholder:text-gray-500 dark:focus:outline-indigo-500`}
                />
                {errors.state_province && (
                  <p className="mt-1 text-sm text-red-600">{errors.state_province.message}</p>
                )}
              </div>
            </div>
            <div className="sm:col-span-2">
              <label htmlFor="postal-code" className="block text-sm/6 font-medium text-gray-900 dark:text-white">
                ZIP / Postal code
              </label>
              <div className="mt-2">
                <input
                  id="zip_postal_code"
                  {...register("zip_postal_code")}
                  type="text"
                  autoComplete="postal-code"
                  className={`block w-full rounded-md bg-white px-3 py-1.5 text-base text-gray-900 outline-1 -outline-offset-1 ${errors.zip_postal_code ? 'outline-red-500' : 'outline-gray-300'} placeholder:text-gray-400 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-600 sm:text-sm/6 dark:bg-white/5 dark:text-white dark:outline-white/10 dark:placeholder:text-gray-500 dark:focus:outline-indigo-500`}
                />
                {errors.zip_postal_code && (
                  <p className="mt-1 text-sm text-red-600">{errors.zip_postal_code.message}</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 flex items-center justify-end gap-x-6">
        <button type="button" className="text-sm/6 font-semibold text-gray-900 dark:text-white">
          Cancel
        </button>
        <button
          type="submit"
          disabled={isSubmitting || !isDirty || !isValid}
          className={`rounded-md px-3 py-2 text-sm font-semibold text-white shadow-xs focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:shadow-none dark:focus-visible:outline-indigo-500 ${
            isSubmitting || !isDirty || !isValid
              ? 'bg-indigo-400 cursor-not-allowed'
              : 'bg-indigo-600 hover:bg-indigo-500 dark:bg-indigo-500'
          }`}
        >
          {isSubmitting ? 'Saving...' : 'Save'}
        </button>
      </div>
    </Form>
  )
}
