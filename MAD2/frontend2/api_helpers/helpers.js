export async function fetchCategories() {
      try {
        const response = await fetch('http://127.0.0.1:5003/api/category');

        const data = await response.json();
        if (!response.ok) {
          throw data;
        }
        return data
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    }