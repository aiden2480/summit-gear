import { useState, useCallback } from "react";

// Manages a stack of toast notifications that auto-dismiss after 3 seconds.
// Each toast gets a unique ID so concurrent toasts can be removed independently.
export default function useToast() {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = "success") => {
    const id = Date.now() + Math.random();
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 3000);
  }, []);

  return { toasts, addToast };
}
