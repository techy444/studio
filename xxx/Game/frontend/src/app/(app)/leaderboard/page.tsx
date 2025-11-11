import { placeholderUsers } from '@/lib/placeholder-data';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Crown } from 'lucide-react';

export default function LeaderboardPage() {
  const topThree = placeholderUsers.slice(0, 3);
  const rest = placeholderUsers.slice(3);

  return (
    <div className="container mx-auto py-8">
      <div className="space-y-4 mb-8 text-center">
        <h1 className="text-4xl font-bold font-headline tracking-tight">Leaderboard</h1>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          See who's dominating the arena. Ranks are updated in real-time based on total points.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        {topThree.map((user, index) => (
          <div key={user.id} className={`relative rounded-lg border p-6 flex flex-col items-center gap-4 ${index === 0 ? 'bg-accent/10 border-accent shadow-lg shadow-accent/10 scale-105' : 'bg-card'}`}>
            {index === 0 && <Crown className="absolute -top-4 -right-4 h-8 w-8 text-yellow-400 rotate-12" />}
            <p className={`font-bold text-3xl ${index === 0 ? 'text-yellow-400' : index === 1 ? 'text-gray-300' : 'text-yellow-600'}`}>#{user.rank}</p>
            <Avatar className="h-24 w-24 border-4 border-background">
              <AvatarImage src={user.avatar} alt={user.username} data-ai-hint="avatar" />
              <AvatarFallback>{user.username.charAt(0).toUpperCase()}</AvatarFallback>
            </Avatar>
            <h3 className="text-xl font-bold">{user.username}</h3>
            <p className="text-2xl font-bold text-accent">{user.totalPoints} <span className="text-sm text-muted-foreground">points</span></p>
            <div className="flex gap-4 text-sm text-muted-foreground">
                <span>Wins: {user.wins}</span>
                <span>Losses: {user.losses}</span>
            </div>
          </div>
        ))}
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[80px]">Rank</TableHead>
            <TableHead>User</TableHead>
            <TableHead className="text-right">Total Points</TableHead>
            <TableHead className="text-right">Wins</TableHead>
            <TableHead className="text-right">Losses</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {rest.map((user) => (
            <TableRow key={user.id}>
              <TableCell className="font-medium text-lg">#{user.rank}</TableCell>
              <TableCell>
                <div className="flex items-center gap-3">
                  <Avatar className="h-10 w-10">
                    <AvatarImage src={user.avatar} alt={user.username} data-ai-hint="avatar" />
                    <AvatarFallback>{user.username.charAt(0).toUpperCase()}</AvatarFallback>
                  </Avatar>
                  <span className="font-medium">{user.username}</span>
                </div>
              </TableCell>
              <TableCell className="text-right font-semibold text-accent">{user.totalPoints}</TableCell>
              <TableCell className="text-right text-green-400">{user.wins}</TableCell>
              <TableCell className="text-right text-red-400">{user.losses}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
