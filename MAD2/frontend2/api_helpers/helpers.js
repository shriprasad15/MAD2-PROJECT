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
export async function fetchPendingCategories() {
  try {
    const response = await fetch('http://127.0.0.1:5003/api/pending-category',{
      method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token':JSON.parse(sessionStorage.getItem('token'))
        }
    });
    const data = await response.json();
    if (!response.ok) {

      throw data;
    }

    return data
  } catch (error) {
    console.error('Error fetching categories:', error);
  }
}

export async function fetchProducts() {
      try {
        const response = await fetch('http://127.0.0.1:5003/api/products');
        const data = await response.json();
        // console.log(data)
        if (response.ok) {
          return data;
        } else {
          console.error('Failed to fetch products');
        }
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    }


export async function fetchProductsByCategory(item_id) {
  try {
    const response = await fetch(`http://127.0.0.1:5003/api/product/cat/${item_id}`);
    const data = await response.json();
    // console.log(data)
    if (response.ok) {
      return data;
    } else {
      console.error('Failed to fetch products');
    }
  } catch (error) {
    console.error('Error fetching products:', error);
  }
}

export async function deleteProductById(itemId) {
  try {
    const response = await fetch(`http://127.0.0.1:5003/api/product/${itemId}`, {
      method: 'DELETE',
    });

    if (response.ok) {
      return response
    } else {
      const errorData = await response.json();
      throw new Error(`Failed to delete product. ${errorData.message}`);
    }
  } catch (error) {
    return { success: false, message: `Error deleting product: ${error.message}` };
  }
}

export async function updateProduct(productId, productData) {
  try {
    const response = await fetch(`http://127.0.0.1:5003/api/product/${productId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(productData),
    });
    return {
      ok: response.ok,
      data: await response.json(),
    };
  } catch (error) {
    console.error('Error updating product:', error);
    throw error;
  }
}

export async function fetchPendingManagers() {
      try {
        const response = await fetch('http://127.0.0.1:5003/api/pending-managers');

        const data = await response.json();
        if (!response.ok) {
          throw data;
        }
        return data
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    }
