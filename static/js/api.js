(function () {
  async function request(path, options = {}) {
    const response = await fetch(path, {
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        ...(options.headers || {}),
      },
      ...options,
    });

    const payload = await response.json().catch(() => ({
      success: false,
      message: "The server returned an invalid response.",
    }));

    if (!response.ok || !payload.success) {
      const error = new Error(payload.message || "Request failed.");
      error.payload = payload;
      throw error;
    }

    return payload.data;
  }

  window.api = { request };
})();
