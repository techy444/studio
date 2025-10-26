"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Swords, RefreshCw } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar';
import { placeholderUsers } from '@/lib/placeholder-data';

export default function BattlePage() {
    const [isSearching, setIsSearching] = useState(false);
    const router = useRouter();

    const currentUser = placeholderUsers[0];
    const opponent = placeholderUsers[1];

    const handleFindMatch = () => {
        setIsSearching(true);
        // Simulate matchmaking
        setTimeout(() => {
            // Navigate to a mock match room
            router.push('/battle/match-123');
        }, 3000);
    };
    
    return (
        <div className="container mx-auto flex items-center justify-center flex-1 py-8">
            <div className="w-full max-w-md text-center">
                <h1 className="text-4xl font-bold font-headline tracking-tight mb-4">Battle Arena</h1>
                <p className="text-muted-foreground mb-8">
                    Challenge a random opponent to a real-time coding duel. First to solve wins!
                </p>

                {isSearching ? (
                    <Card className="p-8">
                        <CardContent className="flex flex-col items-center gap-6 pt-6">
                            <div className="flex items-center justify-center gap-8">
                                <Avatar className="h-20 w-20">
                                    <AvatarImage src={currentUser.avatar} data-ai-hint="avatar" />
                                    <AvatarFallback>{currentUser.username[0]}</AvatarFallback>
                                </Avatar>
                                <Swords className="h-12 w-12 text-accent animate-pulse" />
                                <Avatar className="h-20 w-20">
                                    <AvatarImage src={opponent.avatar} data-ai-hint="avatar" />
                                    <AvatarFallback>{opponent.username[0]}</AvatarFallback>
                                </Avatar>
                            </div>
                            <div className="flex items-center gap-2 text-xl font-semibold">
                                <RefreshCw className="h-5 w-5 animate-spin" />
                                Finding worthy opponent...
                            </div>
                            <p className="text-sm text-muted-foreground">Match Found! Starting in 3... 2... 1...</p>
                        </CardContent>
                    </Card>
                ) : (
                    <Button size="lg" className="w-full h-16 text-xl" onClick={handleFindMatch}>
                        <Swords className="mr-4 h-6 w-6" />
                        Find Match
                    </Button>
                )}
            </div>
        </div>
    );
}
