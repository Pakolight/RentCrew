'use client'
import type {ReactNode, SyntheticEvent} from 'react'
import React, {useRef, useEffect} from 'react'
import {isDialogOpen} from '../signals'
import { useSignals } from '@preact/signals-react/runtime';
import { Form} from "react-router";


interface DrawerProps {
  children: ReactNode;
  method: string;
  action: string;
}

interface DialogProps {
  children: ReactNode;
  transition?: boolean;
  className?: string;
}

const DialogPanel = ({ className, children, transition = false }: DialogProps ) => {
  return (
    <div className={className}>
      {children}
    </div>
  );
};

const DialogTitle = ({ className, children }: {className: string, children: ReactNode}) => {
  return (
    <h2 className={className}>
      {children}
    </h2>
  );
};

// Custom SVG icons to replace the imported ones
const XMarkIcon = ({ className = "", "aria-hidden": ariaHidden = "true" }) => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className={className} aria-hidden={ariaHidden}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
  </svg>
);






export default function Drawer({children, method, action}: DrawerProps) {
  useSignals()

  const dialogRef = useRef<HTMLDialogElement | null>(null);

  useEffect(() => {
    const dialog = dialogRef.current;
    if (!dialog) return;
    if (isDialogOpen.value) {
      if (!dialog.open) {
        try {
          dialog.showModal();
        } catch (e) {
          console.error('dialog.showModal error', e);
        }
      }
    } else {
      if (dialog.open) {
        dialog.close();
      }
    }
  }, [isDialogOpen.value]);

  const handleCancel = (e: SyntheticEvent) => {
    e.preventDefault();
    isDialogOpen.value = false;
  }

  return (
    <div>
      <dialog
          ref={dialogRef}
          onCancel={(e)=> handleCancel(e)}
          className="relative z-30">
        <div className="fixed inset-0" />
        <Form method={method} action={action}  className="fixed inset-0 overflow-hidden">
          <div className="absolute inset-0 overflow-hidden">
            <div className="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10 sm:pl-16">
              <DialogPanel
                transition
                className="pointer-events-auto w-screen max-w-md transform transition duration-500 ease-in-out data-closed:translate-x-full sm:duration-700"
              >
                <div className="relative flex h-full flex-col divide-y divide-gray-200 bg-white shadow-xl dark:divide-white/10 dark:bg-gray-800 dark:after:absolute dark:after:inset-y-0 dark:after:left-0 dark:after:w-px dark:after:bg-white/10">
                  <div className="h-0 flex-1 overflow-y-auto">
                    <div className="bg-indigo-700 px-4 py-6 sm:px-6 dark:bg-indigo-800">
                      <div className="flex items-center justify-between">
                        <DialogTitle className="text-base font-semibold text-white">New project</DialogTitle>
                        <div className="ml-3 flex h-7 items-center">
                          <button
                            type="button"
                            onClick={() => {isDialogOpen.value = false}}
                            className="relative rounded-md text-indigo-200 hover:text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white dark:text-indigo-300 dark:hover:text-white"
                          >
                            <span className="absolute -inset-2.5" />
                            <span className="sr-only">Close panel</span>
                            <XMarkIcon aria-hidden="true" className="size-6" />
                          </button>
                        </div>
                      </div>
                      <div className="mt-1">
                        <p className="text-sm text-indigo-300">
                          Добавление нового оборудования, устройства илн коммутации в ваш склад
                        </p>
                      </div>
                    </div>
                    {
                      children
                    }
                  </div>
                  <div className="flex shrink-0 justify-end px-4 py-4">
                    <button
                      type="button"
                      onClick={() => isDialogOpen.value = false}
                      className="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs inset-ring inset-ring-gray-300 hover:bg-gray-50 dark:bg-white/10 dark:text-gray-100 dark:shadow-none dark:inset-ring-white/5 dark:hover:bg-white/20"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      className="ml-4 inline-flex justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 dark:bg-indigo-500 dark:shadow-none dark:hover:bg-indigo-400 dark:focus-visible:outline-indigo-500"
                    >
                      Save
                    </button>
                  </div>
                </div>
              </DialogPanel>
            </div>
          </div>
        </Form>
      </dialog>
    </div>
  )
}
