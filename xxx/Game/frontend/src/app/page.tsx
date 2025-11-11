import Link from "next/link";
import { ArrowRight, Code, Swords, BarChart3, BotMessageSquare } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Logo } from "@/components/icons";

const features = [
  {
    title: "Practice Arena",
    description: "Hone your skills with a vast library of coding problems.",
    icon: Code,
    href: "/practice",
    cta: "Start Practicing"
  },
  {
    title: "Real-Time Battles",
    description: "Challenge peers to a live coding duel and prove your mettle.",
    icon: Swords,
    href: "/battle",
    cta: "Find a Match"
  },
  {
    title: "Global Leaderboard",
    description: "Climb the ranks and see how you stack up against the best.",
    icon: BarChart3,
    href: "/leaderboard",
    cta: "View Standings"
  },
  {
    title: "AI Code Explainer",
    description: "Get senior-engineer-level explanations for any code snippet.",
    icon: BotMessageSquare,
    href: "/explainer",
    cta: "Explain Code"
  }
]

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen bg-background">
      <main className="flex-1">
        <section className="w-full py-20 md:py-32 lg:py-40">
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-1 lg:gap-12 xl:grid-cols-1">
              <div className="flex flex-col justify-center space-y-4 text-center">
                <div className="space-y-2">
                  <div className="inline-block rounded-lg bg-secondary px-3 py-1 text-sm text-secondary-foreground">
                    Powered by Firebase & GenAI
                  </div>
                  <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl lg:text-7xl font-headline">
                    Welcome to <span className="text-accent">CodeDuel Arena</span>
                  </h1>
                  <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
                    The ultimate platform for competitive programming. Practice problems, challenge others in real-time, and climb the global leaderboard.
                  </p>
                </div>
                <div className="w-full max-w-sm mx-auto space-y-3">
                    <Link href="/login">
                      <Button size="lg" className="w-full" data-testid="enter-arena-button">
                        Enter the Arena <ArrowRight className="ml-2 h-5 w-5" />
                      </Button>
                    </Link>
                    <p className="text-sm text-muted-foreground text-center">
                      Sign in or create an account to get started
                    </p>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        <section className="w-full py-12 md:py-24 lg:py-32 bg-secondary/20">
          <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
              <div className="space-y-2">
                <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl font-headline">Choose Your Challenge</h2>
                <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  Whether you're looking to practice, compete, or learn, we've got you covered.
                </p>
              </div>
            </div>
            <div className="mx-auto grid max-w-5xl grid-cols-1 gap-6 py-12 sm:grid-cols-2 lg:grid-cols-2">
              {features.map((feature) => (
                <Card key={feature.title} className="transform transition-transform duration-300 hover:scale-105 hover:shadow-accent/20 hover:shadow-lg">
                  <CardHeader className="flex flex-row items-center gap-4">
                     <div className="bg-accent/10 p-3 rounded-full">
                        <feature.icon className="h-6 w-6 text-accent" />
                     </div>
                     <CardTitle className="font-headline text-2xl">{feature.title}</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <CardDescription>{feature.description}</CardDescription>
                    <Link href={feature.href}>
                      <Button variant="outline" className="w-full">
                        {feature.cta}
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </section>

        <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t">
          <div className="flex items-center gap-2">
            <Logo className="h-6 w-6" />
            <p className="text-xs text-muted-foreground">&copy; 2024 CodeDuel Arena. All rights reserved.</p>
          </div>
          <nav className="sm:ml-auto flex gap-4 sm:gap-6">
            <Link className="text-xs hover:underline underline-offset-4" href="#">
              Terms of Service
            </Link>
            <Link className="text-xs hover:underline underline-offset-4" href="#">
              Privacy
            </Link>
          </nav>
        </footer>
      </main>
    </div>
  );
}
