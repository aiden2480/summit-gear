import { useState, useEffect } from "react";
import "./ProductModal.css";

const EMPTY_FORM = { name: "", description: "", price: "", image_url: "", category: "", stock: "" };

export default function ProductModal({ open, product, onClose, onSave }) {
  const [form, setForm] = useState(EMPTY_FORM);
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);
  const isEdit = !!product;

  useEffect(() => {
    if (product) {
      setForm({
        name: product.name,
        description: product.description,
        price: String(product.price),
        image_url: product.image_url,
        category: product.category,
        stock: String(product.stock),
      });
    } else {
      setForm(EMPTY_FORM);
    }
    setErrors({});
  }, [product, open]);

  const validate = () => {
    const errs = {};
    if (!form.name.trim()) errs.name = "Name is required";
    if (!form.description.trim()) errs.description = "Description is required";
    if (!form.price || Number(form.price) <= 0) errs.price = "Valid price is required";
    if (!form.image_url.trim()) errs.image_url = "Image URL is required";
    if (!form.category.trim()) errs.category = "Category is required";
    if (form.stock === "" || Number(form.stock) < 0) errs.stock = "Valid stock is required";
    return errs;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return;
    }
    setSaving(true);
    try {
      await onSave({
        name: form.name.trim(),
        description: form.description.trim(),
        price: parseFloat(form.price),
        image_url: form.image_url.trim(),
        category: form.category.trim(),
        stock: parseInt(form.stock, 10),
      });
      onClose();
    } catch {
      setErrors({ form: "Failed to save product. Please try again." });
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (field) => (e) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }));
    if (errors[field]) setErrors((prev) => ({ ...prev, [field]: undefined }));
  };

  if (!open) return null;

  return (
    <>
      <div className="modal-overlay" onClick={onClose} aria-hidden="true" />
      <div className="modal" role="dialog" aria-modal="true" aria-label={isEdit ? "Edit product" : "Add product"}>
        <div className="modal__header">
          <h2 className="modal__title">{isEdit ? "Edit Product" : "Add New Product"}</h2>
          <button className="modal__close" onClick={onClose} aria-label="Close dialog">✕</button>
        </div>
        <form className="modal__form" onSubmit={handleSubmit} noValidate>
          {errors.form && <p className="modal__error">{errors.form}</p>}

          <div className="form-group">
            <label htmlFor="prod-name">Name</label>
            <input id="prod-name" value={form.name} onChange={handleChange("name")} aria-invalid={!!errors.name} />
            {errors.name && <span className="form-error">{errors.name}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="prod-desc">Description</label>
            <textarea id="prod-desc" rows={3} value={form.description} onChange={handleChange("description")} aria-invalid={!!errors.description} />
            {errors.description && <span className="form-error">{errors.description}</span>}
          </div>

          <div className="form-row">
             <div className="form-group">
              <label htmlFor="prod-price">Price ($)</label>
              <input id="prod-price" type="number" step="0.01" min="0" value={form.price} onChange={handleChange("price")} aria-invalid={!!errors.price} readOnly disabled />
              {errors.price && <span className="form-error">{errors.price}</span>}
            </div>
            <div className="form-group">
              <label htmlFor="prod-stock">Stock</label>
              <input id="prod-stock" type="number" min="0" value={form.stock} onChange={handleChange("stock")} aria-invalid={!!errors.stock} />
              {errors.stock && <span className="form-error">{errors.stock}</span>}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="prod-category">Category</label>
            <input id="prod-category" value={form.category} onChange={handleChange("category")} aria-invalid={!!errors.category} />
            {errors.category && <span className="form-error">{errors.category}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="prod-img">Image URL</label>
            <input id="prod-img" type="url" value={form.image_url} onChange={handleChange("image_url")} aria-invalid={!!errors.image_url} />
            {errors.image_url && <span className="form-error">{errors.image_url}</span>}
          </div>

          <div className="modal__actions">
            <button type="button" className="btn btn--secondary" onClick={onClose}>Cancel</button>
            <button type="submit" className="btn btn--primary" disabled={saving}>
              {saving ? "Saving..." : isEdit ? "Update Product" : "Add Product"}
            </button>
          </div>
        </form>
      </div>
    </>
  );
}
