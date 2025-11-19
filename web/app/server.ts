import { createCookieSessionStorage } from "react-router";

type SessionData = {
    userId: string;
    itemId?: string;
};

type SessionFlashData = {
    error: string;
};

const { getSession, commitSession, destroySession } =
    createCookieSessionStorage({
        cookie: {
            name: '__session',
            secrets: [import.meta.env.VITE_SESSION_SECRET],
            sameSite: 'lax',
            path: '/',
            secure: true,
            httpOnly: true,
            maxAge: 60 * 60 * 24 * 30,
        },
    });

export { getSession, commitSession, destroySession };
