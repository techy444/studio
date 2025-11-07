"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Medal, BarChart, Target, Eye, EyeOff, Save, Loader2 } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { getAuthUser, getAuthToken, setAuthData } from '@/lib/auth';

export default function ProfilePage() {
    const [user, setUser] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isSaving, setIsSaving] = useState(false);
    const [showApiKey, setShowApiKey] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        gemini_api_key: ''
    });
    const router = useRouter();
    const { toast } = useToast();

    useEffect(() => {
        const fetchProfile = async () => {
            const token = getAuthToken();
            if (!token) {
                router.push('/login');
                return;
            }

            try {
                const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';
                const response = await fetch(`${API_URL}/api/profile`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch profile');
                }

                const data = await response.json();
                setUser(data);
                setFormData({
                    name: data.name || '',
                    gemini_api_key: data.gemini_api_key || ''
                });
            } catch (error) {
                toast({
                    title: 'Error',
                    description: 'Failed to load profile',
                    variant: 'destructive'
                });
            } finally {
                setIsLoading(false);
            }
        };

        fetchProfile();
    }, [router, toast]);

    const handleSave = async () => {
        setIsSaving(true);
        const token = getAuthToken();

        try {
            const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';
            const response = await fetch(`${API_URL}/api/profile`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Failed to update profile');
            }

            const data = await response.json();
            
            // Update local storage with new user data
            setAuthData(token!, data.user);
            setUser(data.user);

            toast({
                title: 'Success',
                description: 'Profile updated successfully'
            });
        } catch (error) {
            toast({
                title: 'Error',
                description: 'Failed to update profile',
                variant: 'destructive'
            });
        } finally {
            setIsSaving(false);
        }
    };

    if (isLoading) {
        return (
            <div className="container mx-auto py-8 flex items-center justify-center min-h-[50vh]">
                <Loader2 className="h-8 w-8 animate-spin text-accent" />
            </div>
        );
    }

    if (!user) {
        return null;
    }

    const stats = [
        { label: 'Total Points', value: user.total_points, icon: BarChart },
        { label: 'Wins', value: user.wins, icon: Medal },
        { label: 'Losses', value: user.losses, icon: Target },
    ];

    return (
        <div className="container mx-auto py-8 max-w-4xl">
            <div className="flex flex-col items-center space-y-4 mb-12">
                <Avatar className="h-32 w-32 border-4 border-accent">
                    <AvatarImage 
                        src={`https://picsum.photos/seed/${user.id}/150/150`} 
                        alt={user.username} 
                        data-ai-hint="avatar" 
                    />
                    <AvatarFallback className="text-4xl">
                        {user.username.charAt(0).toUpperCase()}
                    </AvatarFallback>
                </Avatar>
                <h1 className="text-4xl font-bold font-headline" data-testid="profile-username">
                    {user.username}
                </h1>
                <p className="text-muted-foreground">{user.email}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
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

            <Card>
                <CardHeader>
                    <CardTitle>Profile Settings</CardTitle>
                    <CardDescription>
                        Update your personal information and configure API settings
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    <div className="space-y-2">
                        <Label htmlFor="name">Full Name</Label>
                        <Input
                            id="name"
                            data-testid="name-input"
                            placeholder="Enter your full name"
                            value={formData.name}
                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            disabled={isSaving}
                        />
                        <p className="text-xs text-muted-foreground">
                            Your display name for the platform
                        </p>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="email">Email</Label>
                        <Input
                            id="email"
                            data-testid="email-display"
                            type="email"
                            value={user.email}
                            disabled
                            className="bg-muted"
                        />
                        <p className="text-xs text-muted-foreground">
                            Email cannot be changed
                        </p>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="gemini-api-key">Gemini API Key</Label>
                        <div className="relative">
                            <Input
                                id="gemini-api-key"
                                data-testid="gemini-api-key-input"
                                type={showApiKey ? "text" : "password"}
                                placeholder="Enter your Gemini API key"
                                value={formData.gemini_api_key}
                                onChange={(e) => setFormData({ ...formData, gemini_api_key: e.target.value })}
                                disabled={isSaving}
                                className="pr-10"
                            />
                            <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                className="absolute right-0 top-0 h-full px-3 hover:bg-transparent"
                                onClick={() => setShowApiKey(!showApiKey)}
                                data-testid="toggle-api-key-visibility"
                            >
                                {showApiKey ? (
                                    <EyeOff className="h-4 w-4 text-muted-foreground" />
                                ) : (
                                    <Eye className="h-4 w-4 text-muted-foreground" />
                                )}
                            </Button>
                        </div>
                        <p className="text-xs text-muted-foreground">
                            Required for AI Code Explainer feature. Get your API key from{' '}
                            <a 
                                href="https://aistudio.google.com/apikey" 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-accent hover:underline"
                            >
                                Google AI Studio
                            </a>
                        </p>
                    </div>

                    <Button 
                        onClick={handleSave} 
                        disabled={isSaving}
                        data-testid="save-profile-button"
                        className="w-full sm:w-auto"
                    >
                        {isSaving ? (
                            <>
                                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                Saving...
                            </>
                        ) : (
                            <>
                                <Save className="mr-2 h-4 w-4" />
                                Save Changes
                            </>
                        )}
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
