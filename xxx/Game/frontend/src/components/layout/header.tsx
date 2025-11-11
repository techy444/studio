"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Code, Swords, BarChart3, BotMessageSquare, Menu } from "lucide-react";

import { cn } from "@/lib/utils";
import { Logo } from "@/components/icons";
import { UserNav } from "./user-nav";
import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from "@/components/ui/sheet";
import { Button } from "../ui/button";

const navItems = [
  { href: "/practice", label: "Practice", icon: Code },
  { href: "/battle", label: "Battle", icon: Swords },
  { href: "/leaderboard", label: "Leaderboard", icon: BarChart3 },
  { href: "/explainer", label: "Explainer", icon: BotMessageSquare },
];

export function Header() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 max-w-screen-2xl items-center">
        <div className="mr-4 hidden md:flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <Logo className="h-6 w-6 text-accent" />
            <span className="hidden font-bold sm:inline-block font-headline">
              CodeDuel Arena
            </span>
          </Link>
          <nav className="flex items-center gap-6 text-sm">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "transition-colors hover:text-foreground/80",
                  pathname?.startsWith(item.href) ? "text-foreground" : "text-foreground/60"
                )}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
        
        <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
          <div className="w-full flex-1 md:w-auto md:flex-none">
            {/* Can add a search bar here later */}
          </div>
          <nav className="flex items-center md:mr-4">
            <UserNav />
          </nav>
        </div>

        {/* Mobile Nav */}
        <div className="flex items-center md:hidden">
            <Sheet>
                <SheetTrigger asChild>
                <Button variant="ghost" size="icon">
                    <Menu className="h-5 w-5"/>
                    <span className="sr-only">Toggle Menu</span>
                </Button>
                </SheetTrigger>
                <SheetContent side="left">
                <Link href="/" className="mr-6 flex items-center space-x-2 mb-6">
                    <Logo className="h-6 w-6 text-accent" />
                    <span className="font-bold font-headline">
                    CodeDuel Arena
                    </span>
                </Link>
                <nav className="flex flex-col gap-4">
                    {navItems.map((item) => (
                    <Link
                        key={item.href}
                        href={item.href}
                        className={cn(
                        "transition-colors hover:text-foreground/80",
                        pathname?.startsWith(item.href) ? "text-foreground font-semibold" : "text-foreground/60"
                        )}
                    >
                        {item.label}
                    </Link>
                    ))}
                </nav>
                </SheetContent>
            </Sheet>
            <Link href="/" className="flex items-center space-x-2 ml-2">
                <Logo className="h-6 w-6 text-accent" />
            </Link>
        </div>
      </div>
    </header>
  );
}
