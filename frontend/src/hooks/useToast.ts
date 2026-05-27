import { useCallback, useState } from "react";
import type { ToastMessage, ToastType } from "../types";

/** Manages a list of short-lived toast notifications that auto-dismiss after 3 seconds. */
export default function useToast() {
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const addToast = useCallback((message: string, type: ToastType = "success") => {
    const id = Date.now() + Math.random();
    setToasts((prev) => [...prev, { id, message, type }]);

    setTimeout(() => {
      setToasts((prev) => prev.filter((toast) => toast.id !== id));
    }, 3000);
  }, []);

  return { toasts, addToast };
}
