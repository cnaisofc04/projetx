import { useState } from 'react';

export default function PhotoUploader({ photos, onPhotosChange, maxPhotos = 6 }) {
  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    const remainingSlots = maxPhotos - photos.length;
    const filesToAdd = files.slice(0, remainingSlots);

    filesToAdd.forEach(file => {
      const reader = new FileReader();
      reader.onloadend = () => {
        onPhotosChange([...photos, reader.result]);
      };
      reader.readAsDataURL(file);
    });
  };

  const removePhoto = (index) => {
    onPhotosChange(photos.filter((_, i) => i !== index));
  };

  return (
    <div className="photo-uploader">
      <h3>Photos ({photos.length}/{maxPhotos}) *</h3>
      <div className="photo-grid">
        {photos.map((photo, index) => (
          <div key={index} className="photo-preview">
            <img src={photo} alt={`Photo ${index + 1}`} />
            <button 
              type="button"
              className="remove-photo" 
              onClick={() => removePhoto(index)}
            >
              ×
            </button>
          </div>
        ))}
        {photos.length < maxPhotos && (
          <label className="add-photo-btn">
            <input
              type="file"
              accept="image/*"
              multiple
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
            <span className="add-icon">+</span>
            <span className="add-text">Ajouter</span>
          </label>
        )}
      </div>
      {photos.length === 0 && (
        <p className="upload-hint">Au moins 1 photo requise</p>
      )}
    </div>
  );
}
