<template>
    <div class="mdl-card login-card mdl-shadow--4dp">
        <div class="mdl-card__title mdl-color--primary mdl-color-text--white">
            <h2 class="mdl-card__title-text">Log in</h2>
        </div>
        <div class="mdl-card__supporting-text">
            <form class="form-signin" method="POST" action="/user/login">
                <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                    <input class="mdl-textfield__input" type="email" id="email" name="email">
                    <label class="mdl-textfield__label" for="email">Email Address</label>
                </div>
                <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
                    <input class="mdl-textfield__input" type="password" id="password" name="password">
                    <label class="mdl-textfield__label" for="password">Password</label>
                </div>
                <button type="submit" class="mdl-button mdl-js-button mdl-button--raised mdl-button--colored ">Sign In</button>
                | <a href="#">Forgot my password</a>
            </form>
        </div>
    </div>
</template>

<style>
.mdl-layout__content {
    align-items: center;
    display: flex;
    justify-content: center;
}
.login-card {
    margin-top: 10px;
}
</style>
