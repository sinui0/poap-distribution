import { IUserProfile, IUserIdentity } from '@/interfaces';

export interface AppNotification {
    content: string;
    color?: string;
    showProgress?: boolean;
}

export interface MainState {
    token: string;
    isLoggedIn: boolean | null;
    logInError: { error: boolean, detail: string | null };
    userProfile: IUserProfile | null;
    userIdentities: IUserIdentity[];
    dashboardMiniDrawer: boolean;
    dashboardShowDrawer: boolean;
    notifications: AppNotification[];
}
