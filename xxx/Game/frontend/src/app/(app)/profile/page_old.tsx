import { placeholderUsers } from '@/lib/placeholder-data';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Medal, BarChart, Target } from 'lucide-react';

export default function ProfilePage() {
    const user = placeholderUsers[0]; // Mock current user

    const stats = [
        { label: 'Rank', value: `#${user.rank}`, icon: Medal },
        { label: 'Total Points', value: user.totalPoints, icon: BarChart },
        { label: 'Win Rate', value: `${((user.wins / (user.wins + user.losses)) * 100).toFixed(1)}%`, icon: Target },
    ]

    return (
        <div className="container mx-auto py-8">
            <div className="flex flex-col items-center space-y-4 mb-12">
                <Avatar className="h-32 w-32 border-4 border-accent">
                    <AvatarImage src={user.avatar} alt={user.username} data-ai-hint="avatar" />
                    <AvatarFallback className="text-4xl">{user.username.charAt(0).toUpperCase()}</AvatarFallback>
                </Avatar>
                <h1 className="text-4xl font-bold font-headline">{user.username}</h1>
                <p className="text-muted-foreground">{user.wins} Wins / {user.losses} Losses</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {stats.map((stat, index) => (
                    <Card key={index}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">{stat.label}</CardTitle>
                            <stat.icon className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{stat.value}</div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            <div className="mt-12">
                <h2 className="text-2xl font-bold font-headline mb-4">Badges</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    {/* Placeholder for badges */}
                    <div className="flex flex-col items-center gap-2 p-4 border rounded-lg bg-card">
                        <Medal className="h-10 w-10 text-yellow-400" />
                        <p className="text-sm font-semibold">Rising Coder</p>
                    </div>
                     <div className="flex flex-col items-center gap-2 p-4 border rounded-lg bg-card">
                        <Medal className="h-10 w-10 text-gray-300" />
                        <p className="text-sm font-semibold">Speedster</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
