const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// ============ Types ============

export interface Certificate {
  id: string;
  code: string;
  recipientName: string;
  email: string;
  workshopName: string;
  issueDate: string;
  skills: string[];
  instructor: string;
  isVerified: boolean;
  createdAt: string;
}

export interface CertificateVerifyResponse {
  id: string;
  code: string;
  recipientName: string;
  workshopName: string;
  issueDate: string;
  skills: string[];
  instructor: string;
  isVerified: boolean;
}

export interface Workshop {
  id: string;
  title: string;
  date: string;
  description?: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced';
  instructor: string;
  image?: string;
  createdAt: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

// ============ Auth ============

export async function loginAdmin(email: string, password: string): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    throw new Error('Login failed');
  }

  return response.json();
}

export async function registerAdmin(email: string, password: string): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    throw new Error('Registration failed');
  }

  return response.json();
}

// ============ Certificates (Public) ============

export async function verifyCertificate(code: string): Promise<CertificateVerifyResponse> {
  const response = await fetch(`${API_BASE_URL}/api/certificates/verify/${code.toUpperCase()}`);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('Certificate not found');
    }
    throw new Error('Verification failed');
  }

  return response.json();
}

export async function searchCertificates(email: string): Promise<CertificateVerifyResponse[]> {
  const response = await fetch(`${API_BASE_URL}/api/certificates/search?email=${encodeURIComponent(email)}`);

  if (!response.ok) {
    throw new Error('Search failed');
  }

  return response.json();
}

// ============ Certificates (Admin) ============

export async function createCertificate(
  token: string,
  certificate: Omit<Certificate, 'id' | 'code' | 'isVerified' | 'createdAt'>
): Promise<Certificate> {
  const response = await fetch(`${API_BASE_URL}/api/certificates/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(certificate),
  });

  if (!response.ok) {
    throw new Error('Failed to create certificate');
  }

  return response.json();
}

export async function getAllCertificates(token: string, skip: number = 0, limit: number = 100): Promise<Certificate[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/certificates/admin/all?skip=${skip}&limit=${limit}`,
    {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error('Failed to fetch certificates');
  }

  return response.json();
}

export async function getCertificateDetail(token: string, certificateId: string): Promise<Certificate> {
  const response = await fetch(`${API_BASE_URL}/api/certificates/admin/${certificateId}`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch certificate');
  }

  return response.json();
}

export async function updateCertificate(
  token: string,
  certificateId: string,
  updates: Partial<Certificate>
): Promise<Certificate> {
  const response = await fetch(`${API_BASE_URL}/api/certificates/admin/${certificateId}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updates),
  });

  if (!response.ok) {
    throw new Error('Failed to update certificate');
  }

  return response.json();
}

export async function deleteCertificate(token: string, certificateId: string): Promise<{ success: true; message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/certificates/admin/${certificateId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('Failed to delete certificate');
  }

  return response.json();
}

export async function bulkCreateCertificates(
  token: string,
  certificates: Array<Omit<Certificate, 'id' | 'code' | 'isVerified' | 'createdAt'>>
): Promise<{ success: boolean; count: number; certificates: Certificate[] }> {
  const response = await fetch(`${API_BASE_URL}/api/certificates/admin/bulk-create`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(certificates),
  });

  if (!response.ok) {
    throw new Error('Failed to create certificates');
  }

  return response.json();
}

export async function getCertificateStats(token: string): Promise<{ total_certificates: number }> {
  const response = await fetch(`${API_BASE_URL}/api/certificates/admin/stats`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch statistics');
  }

  return response.json();
}

// ============ Workshops (Public) ============

export async function getWorkshops(skip: number = 0, limit: number = 100): Promise<Workshop[]> {
  const response = await fetch(`${API_BASE_URL}/api/workshops?skip=${skip}&limit=${limit}`);

  if (!response.ok) {
    throw new Error('Failed to fetch workshops');
  }

  return response.json();
}

export async function getWorkshopDetail(workshopId: string): Promise<Workshop> {
  const response = await fetch(`${API_BASE_URL}/api/workshops/${workshopId}`);

  if (!response.ok) {
    throw new Error('Failed to fetch workshop');
  }

  return response.json();
}

// ============ Workshops (Admin) ============

export async function createWorkshop(token: string, workshop: Omit<Workshop, 'id' | 'createdAt'>): Promise<Workshop> {
  const response = await fetch(`${API_BASE_URL}/api/workshops/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(workshop),
  });

  if (!response.ok) {
    throw new Error('Failed to create workshop');
  }

  return response.json();
}

export async function updateWorkshop(
  token: string,
  workshopId: string,
  updates: Partial<Workshop>
): Promise<Workshop> {
  const response = await fetch(`${API_BASE_URL}/api/workshops/${workshopId}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updates),
  });

  if (!response.ok) {
    throw new Error('Failed to update workshop');
  }

  return response.json();
}

export async function deleteWorkshop(token: string, workshopId: string): Promise<{ success: true; message: string }> {
  const response = await fetch(`${API_BASE_URL}/api/workshops/${workshopId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('Failed to delete workshop');
  }

  return response.json();
}
