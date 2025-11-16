// To create a user
interface UserCreateInput {
    email: string;
    password: string;
    first_name?: string;
    last_name?: string;
    role: string;
    company?: number | null;
    avatar?: File | null;
}

// For user update
interface UserUpdateInput {
    email?: string;
    first_name?: string;
    last_name?: string;
    role?: string;
    is_active?: boolean;
    is_staff?: boolean;
    company?: number | null;
    avatar?: File | null;
}

// to create a company
interface CompanyCreateInput {
    legalName: string;
    tradeName?: string;
    vatNumber?: string;
    iban?: string;
    currency?: string;
    logo?: File;
    country: string;
    street_address: string;
    city: string;
    state_province: string;
    zip_postal_code: string;
    owner: number;
}

// For company renewal
interface CompanyUpdateInput {
    legalName?: string;
    tradeName?: string;
    vatNumber?: string;
    iban?: string;
    currency?: string;
    logo?: File;
    country?: string;
    street_address?: string;
    city?: string;
    state_province?: string;
    zip_postal_code?: string;
}