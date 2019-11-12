class ApiInterface {
    apiEndpoint = '/api'

    async getCurrentUser(): Promise<any> {
        const response = await fetch(`${this.apiEndpoint}/users/current_user`)
        const userJson = await response.json()
        if (userJson.success) {
            return {
                isAuthenticated: true,
                id: userJson.user.id,
                email: userJson.user.email,
                teacher_name: userJson.user.teacher_name,
            }
        } else {
            return {
                isAuthenticated: false,
                id: '',
                email: '',
                teacher_name: '',
            }
        }

    }
}

export default ApiInterface;