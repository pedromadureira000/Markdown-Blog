import { helpers} from "vuelidate/lib/validators";
export const slugFieldValidator = helpers.regex('alphaNumDashAndUnderline', /^[a-z\d-_]*$/i)
