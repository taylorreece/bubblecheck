import React from "react";
import {AuthConsumer} from "../contexts/AuthContext";

const BCDrawer: React.FC = () => {
    return (
        <div>
            <AuthConsumer>
                {(authctx) => <div>
			<strong>Email:</strong> { authctx.user.email }<br />
			<strong>Name:</strong> { authctx.user.teacher_name }<br />
			<strong>UserID:</strong> { authctx.user.usersid }<br />
		</div>}
            </AuthConsumer>
        </div>
    );
};

export default BCDrawer;
