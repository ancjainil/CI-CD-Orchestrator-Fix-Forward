export function useAuthClient() {
  const clientId = process.env.NEXT_PUBLIC_GITHUB_CLIENT_ID;
  const appUrl = process.env.NEXT_PUBLIC_APP_URL || (typeof window !== "undefined" ? window.location.origin : "");
  const redirectUri = `${appUrl}/oauth/callback`;
  const loginUrl = clientId
    ? `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${encodeURIComponent(
        redirectUri,
      )}&scope=read:user,repo`
    : "/dashboard?devLogin=1";
  return { loginUrl };
}
