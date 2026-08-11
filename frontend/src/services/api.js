const apiBase = '/api';

export const fetchApi = async (url, token, options = {}) => {
  options.headers = {
    ...options.headers,
    'Authorization': `Bearer ${token}`
  };
  const res = await fetch(`${apiBase}${url}`, options);
  if (!res.ok) {
    if (res.status === 401) throw new Error("UNAUTHORIZED");
    throw new Error(`API Error: ${res.status}`);
  }
  return res.json();
};

export const apiBaseUrl = apiBase;
