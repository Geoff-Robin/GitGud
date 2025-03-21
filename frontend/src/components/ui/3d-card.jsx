import React, { createContext, useContext, useRef, useState } from "react";

// Context for 3D Card effect
const MouseEnterContext = createContext(null);

// Card Container Component
export const CardContainer = ({ children, className, ...props }) => {
  const containerRef = useRef(null);
  const [isMouseEntered, setIsMouseEntered] = useState(false);

  const handleMouseMove = (e) => {
    if (!containerRef.current) return;
    const { left, top, width, height } = containerRef.current.getBoundingClientRect();
    const x = (e.clientX - left - width / 2) / 25;
    const y = (e.clientY - top - height / 2) / 25;
    containerRef.current.style.transform = `rotateY(${x}deg) rotateX(${-y}deg)`;
  };

  const handleMouseEnter = () => {
    setIsMouseEntered(true);
    if (!containerRef.current) return;
    containerRef.current.style.transition = "transform 0.3s ease-out";
  };

  const handleMouseLeave = () => {
    setIsMouseEntered(false);
    if (!containerRef.current) return;
    containerRef.current.style.transition = "transform 0.2s ease-out";
    containerRef.current.style.transform = "rotateY(0deg) rotateX(0deg)";
  };

  return (
    <MouseEnterContext.Provider value={isMouseEntered}>
      <div
        ref={containerRef}
        className={`flex items-center justify-center ${className}`}
        style={{ perspective: "1000px" }}
        onMouseEnter={handleMouseEnter}
        onMouseMove={handleMouseMove}
        onMouseLeave={handleMouseLeave}
        {...props}
      >
        {children}
      </div>
    </MouseEnterContext.Provider>
  );
};

// Card Body Component
export const CardBody = ({ children, className, ...props }) => {
  return (
    <div
      className={`w-full relative ${className}`}
      style={{ transformStyle: "preserve-3d" }}
      {...props}
    >
      {children}
    </div>
  );
};

// Card Item Component
export const CardItem = ({
  as: Component = "div",
  children,
  className,
  translateX = 0,
  translateY = 0,
  translateZ = 0,
  ...props
}) => {
  const isMouseEntered = useContext(MouseEnterContext);

  return (
    <Component
      className={`transition duration-200 ease-linear ${className}`}
      style={{
        transform: isMouseEntered
          ? `translateX(${translateX}px) translateY(${translateY}px) translateZ(${translateZ}px)`
          : "translateZ(0px)",
        transformStyle: "preserve-3d",
      }}
      {...props}
    >
      {children}
    </Component>
  );
};