class ApiInterface {
    public apiEndpoint = "/api";

    public async getCurrentUser(): Promise<any> {
        const response = await fetch(`${this.apiEndpoint}/users/current_user`);
        const userJson = await response.json();
        if (userJson.success) {
            return {
                email: userJson.user.email,
                id: userJson.user.id,
                isAuthenticated: true,
                teacher_name: userJson.user.teacher_name,
            };
        } else {
            return {
                email: "",
                id: "",
                isAuthenticated: false,
                teacher_name: "",
            };
        }
    }
}

export default ApiInterface;
