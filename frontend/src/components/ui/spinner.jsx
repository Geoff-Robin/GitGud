import React from 'react';
import { cn } from '@/lib/utils';
import { cva } from 'class-variance-authority';
import { Loader2 } from 'lucide-react';

const spinnerVariants = cva(
  'flex-col items-center justify-center',
  {
    variants: {
      show: { true: 'flex', false: 'hidden' },
    },
    defaultVariants: { show: true },
  }
);

const loaderVariants = cva(
  'animate-spin text-primary',
  {
    variants: {
      size: {
        small: 'h-6 w-6',
        medium: 'h-8 w-8',
        large: 'h-12 w-12',
      },
    },
    defaultVariants: { size: 'medium' },
  }
);

export default function Spinner({
  size = 'medium',
  show = true,
  children,
  className,
}) {
  return (
    <span className={spinnerVariants({ show })}>
      <Loader2 className={cn(loaderVariants({ size }), className)} />
      {children}
    </span>
  );
}
