import React from 'react';
import {AuthProvider, AuthConsumer} from './contexts/AuthContext'

const App: React.FC = () => {
  return (
    <div>
      <a href="/api/users/oauth/cognito/login">Login</a>
      <a href="/api/users/logout">Logout</a>
      <AuthProvider>
        <AuthConsumer>
          {authctx => <div>
            User Id: { authctx.user.usersid } <br />
            Email: { authctx.user.email } <br />
            Teacher Nmae: {authctx.user.teacher_name } <br />
          </div>}
        </AuthConsumer>
      </AuthProvider>
    </div>
  );
}

export default App;
