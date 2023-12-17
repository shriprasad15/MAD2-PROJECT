import {createRouter, createWebHistory} from 'vue-router'
import Home from "@/views/Home.vue";
import Login from "@/views/User/UserLogin.vue";
import Signup from "@/views/User/UserSignup.vue";
import UserSignup from "@/views/User/UserSignup.vue";
import UserDashboard from "@/views/User/UserDashboard.vue";
import AdminDashboard from "@/views/Admin/AdminDashboard.vue";
import UserLogin from "@/views/User/UserLogin.vue";
import AdminLogin from "@/views/Admin/AdminLogin.vue";
import ManagerLogin from "@/views/Manager/ManagerLogin.vue";
import ManagerSignup from "@/views/Manager/ManagerSignup.vue";
import ManagerDashboard from "@/views/Manager/ManagerDashboard.vue";
import CreateCategory from "@/views/Admin/CreateCategory.vue";
import DeleteCategory from "@/views/Admin/DeleteCategory.vue";
import EditCategory from "@/views/Admin/EditCategory.vue";
import CreateProduct from "@/views/Manager/CreateProduct.vue";
import DeleteProduct from "@/views/Manager/DeleteProduct.vue";
import EditProduct from "@/views/Manager/EditProduct.vue";
import ManagerCreateCategory from "@/views/Manager/CategoryRequests/ManagerCreateCategory.vue";
import ManagerPendingRequests from "@/views/Manager/ManagerPendingRequests.vue";
import AdminCategoryApproval from "@/views/Admin/AdminCategoryApproval.vue";
import ManagerHome from "@/views/Manager/ManagerHome.vue";
import AdminHome from "@/views/Admin/AdminHome.vue";
import ManagerDeleteCategory from "@/views/Manager/CategoryRequests/ManagerDeleteCategory.vue";
import ManagerEditCategory from "@/views/Manager/CategoryRequests/ManagerEditCategory.vue";
import Cart from "@/views/User/Cart.vue";
import UserHome from "@/views/User/UserHome.vue";
import Profile from "@/views/User/Profile.vue";

const routes = [

    {
        path: '/',
        name: 'home',
        component: Home
    },
    // col-sm
    // User Functions
    {
        path: '/user-login',
        name: 'user-login',
        component: UserLogin
    },
    {
        path: '/user-dashboard',
        name: 'user-dashboard',
        component: UserDashboard,
        redirect: '/user-dashboard/home',
        meta: {requiresUser: true},
        children: [
            {
                path: 'home',
                component: UserHome
            },
            {
                path:'Cart',
                name:'cart',
                component: Cart
            },
            {
                path:'Profile',
                name:'profile',
                component: Profile
            }
        ]
    },
    {
        path: '/user-signup',
        name: 'user-signup',
        component: UserSignup
    },

    // Manager Functions
    {
        path: '/manager-login',
        name: 'manager-login',
        component: ManagerLogin
    },
    {
        path: '/manager-signup',
        name: 'manager-signup',
        component: ManagerSignup
    },
    {
        path: '/manager-dashboard',
        name: 'manager-dashboard',
        component: ManagerDashboard,
        meta: {requiresManager: true},
        redirect: '/manager-dashboard/home',
        children: [
            {
                path: 'home',
                component: ManagerHome
            },
            {
                path: 'Create-Product',
                component: CreateProduct
            },
            {
                path: 'Delete-Product',
                name: 'delete-product',
                component: DeleteProduct
            },
            {
                path: 'Edit-Product',
                name: 'edit-product',
                component: EditProduct
            },
            {
                path: 'Create-Category',
                name: 'manager-create-category',
                component: ManagerCreateCategory,

            },
            {
                path: 'Delete-Category',
                name: 'manager-delete-category',
                component: ManagerDeleteCategory,

            },
            {
                path: 'Edit-Category',
                name: 'manager-edit-category',
                component: ManagerEditCategory,
            },
            {
                path: 'Manager-PendingRequests',
                name: 'manager-pending-requests',
                component: ManagerPendingRequests,

            },

        ]


    },


    // Admin Functions
    {
        path: '/admin-login',
        name: 'admin-login',
        component: AdminLogin
    },
    {
        path: '/admin-dashboard',
        name: 'admin-dashboard',
        component: AdminDashboard,
        redirect: '/admin-dashboard/home',
        children: [
            {
                path: 'home',
                component: AdminHome
            },
            {
                path: 'Create-Category',
                name: 'admin-create-category',
                component: CreateCategory
            },
            {
                path: 'Delete-Category',
                name: 'admin-delete-category',
                component: DeleteCategory
            },
            {
                path: 'Edit-Category',
                name: 'admin-edit-category',
                component: EditCategory
            },
            {
                path: 'Approve-Requests',
                name: 'admin-approve-category',
                component: AdminCategoryApproval
            },
        ],
        meta: {requiresAdmin: true},

    },

]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})
router.beforeEach((to, from, next) => {
    const loggedIn = JSON.parse(sessionStorage.getItem('token'))
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin);
    const requiresManager = to.matched.some(record => record.meta.requiresManager);
    const requiresUser = to.matched.some(record => record.meta.requiresUser);
    var role=''
    const check_role = JSON.parse(sessionStorage.getItem("role"));
    console.log(`Require Admin ${requiresAdmin}`)
    console.log(`Logged in ${loggedIn}`)
    console.log(role)
    if(check_role) {
        role = check_role[0];
        next()
    }

        // Check if the route requires authentication
        if (requiresAdmin === true) {

            next()
            console.log(role)
            // Check if the route requires admin access


            if (loggedIn && role === "admin") {
                console.log("is admin")
                next(); // Proceed to the route
            } else {
                console.log(`Role : ${role}, Logged in : ${loggedIn}`)
                next('/admin-login'); // Redirect to admin login if route requires admin access and user is not logged in or not an admin
            }



    } else if (requiresManager) {
        console.log(loggedIn, "man")
        console.log(role, "ro")
        // Check if the route requires manager access
        if (loggedIn && role === "manager") {
            console.log("is_manager")
            next(); // Proceed to the route
        } else {
            next('/manager-login'); // Redirect to manager login if route requires manager access and user is not logged in or not a manager
        }
    }
     else if(requiresUser) {
         console.log(loggedIn)
        console.log(role)
         if (loggedIn && role === "user") {
             console.log("is_user")
            next(); // Proceed to the route
        } else {
            next('/user-login'); // Redirect to manager login if route requires manager access and user is not logged in or not a manager
        }
    }
    else{
        next();
    }
});

export default router
