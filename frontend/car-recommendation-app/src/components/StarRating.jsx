import React from "react";
import { Star } from "lucide-react";

export default function StarRating({ value, onChange, size = 24 }) {
  return (
    <div style={{ display: "flex", gap: "6px", cursor: "pointer" }}>
      {[1, 2, 3, 4, 5].map((star) => {
        const active = star <= value;

        return (
          <Star
            key={star}
            size={size}
            onClick={() => onChange(star)}
            style={{
              fill: active ? "#FFD700" : "none",
              stroke: "#FFD700",
              transition: "fill 0.2s, transform 0.1s",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.2)")}
            onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
          />
        );
      })}
    </div>
  );
}
