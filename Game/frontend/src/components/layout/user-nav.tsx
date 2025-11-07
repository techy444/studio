"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import Link from 'next/link';
import { LogOut, User as UserIcon, LogIn } from "lucide-react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getAuthUser, clearAuthData, isAuthenticated } from "@/lib/auth";
import type { User } from "@/lib/auth";

export function UserNav() {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const user = getAuthUser();
    const authenticated = isAuthenticated();
    setCurrentUser(user);
    setIsLoggedIn(authenticated);
  }, []);

  const handleLogout = () => {
    clearAuthData();
    setCurrentUser(null);
    setIsLoggedIn(false);
    router.push("/");
  };

  if (!isLoggedIn || !currentUser) {
    return (
      <Link href="/login">
        <Button variant="ghost" size="sm" data-testid="login-button">
          <LogIn className="mr-2 h-4 w-4" />
          Sign In
        </Button>
      </Link>
    );
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-8 w-8 rounded-full" data-testid="user-menu-button">
          <Avatar className="h-9 w-9">
            <AvatarImage src={`https://picsum.photos/seed/${currentUser.id}/150/150`} alt={currentUser.username} data-ai-hint="avatar" />
            <AvatarFallback>{currentUser.username.charAt(0).toUpperCase()}</AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="end" forceMount>
        <DropdownMenuLabel className="font-normal">
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium leading-none">{currentUser.username}</p>
            <p className="text-xs leading-none text-muted-foreground">
              {currentUser.email}
            </p>
            <p className="text-xs leading-none text-muted-foreground mt-1">
              Points: {currentUser.total_points} | Wins: {currentUser.wins}
            </p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <Link href="/profile">
            <DropdownMenuItem>
              <UserIcon className="mr-2 h-4 w-4" />
              <span>Profile</span>
            </DropdownMenuItem>
          </Link>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={handleLogout} data-testid="logout-button">
          <LogOut className="mr-2 h-4 w-4" />
          <span>Log out</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
