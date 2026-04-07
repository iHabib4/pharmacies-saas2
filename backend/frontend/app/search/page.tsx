const searchMedicines = async () => {
  const res = await fetch(
    `/api/products/search?q=${query}&lat=${lat}&lon=${lon}`
  );
  const data = await res.json();
  setResults(data);
};
