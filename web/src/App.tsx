import React from "react";
import {AuthConsumer, AuthProvider} from "./contexts/AuthContext";

function PrintUserInfo(props: any) {
  return (
    <div>
      User Id: {props.user.usersid} <br />
      Email: {props.user.email} <br />
      Teacher Name: {props.user.teacher_name} <br />
    </div>
  );
}

const App: React.FC = () => {
  return (
    <div>
      <a href="/api/users/oauth/cognito/login">Login</a>
      <a href="/api/users/logout">Logout</a>
      <AuthProvider>
        <AuthConsumer>
          {(authctx) => <PrintUserInfo user={authctx.user} />}

        </AuthConsumer>
      </AuthProvider>
    </div>
  );
};

export default App;
