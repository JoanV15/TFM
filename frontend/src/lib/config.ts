import { PUBLIC_BACKEND_URL } from '$env/static/public';

if (!PUBLIC_BACKEND_URL) {
    throw new Error("❌ PUBLIC_BACKEND_URL no está definida. Revisa tu archivo .env");
}

export { PUBLIC_BACKEND_URL };

