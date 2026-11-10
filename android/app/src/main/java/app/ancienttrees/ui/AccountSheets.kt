// Signing in and the account, each in one bottom sheet (CLAUDE.md, "One sheet for
// every overlay"). The words are the website's sign-in copy
// (site/src/lib/signin-strings.ts) in every language; the route is the iPhone's:
// Google, or an emailed link that brings the person back to the app.

package app.ancienttrees.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.fromHtml
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import app.ancienttrees.R
import app.ancienttrees.account.Account
import app.ancienttrees.account.Problem
import app.ancienttrees.account.SignIn
import kotlinx.coroutines.launch

@Composable
private fun SheetTitle(text: String) {
    Text(text, fontFamily = Brand, fontWeight = FontWeight.Bold, fontSize = 26.sp, lineHeight = 31.sp)
}

@Composable
private fun problemText(p: Problem): String = stringResource(
    when (p) {
        Problem.NOT_AN_EMAIL -> R.string.problem_not_email
        Problem.COULD_NOT_SEND -> R.string.problem_send
        Problem.LINK_USED -> R.string.problem_link
        Problem.GOOGLE_OFF -> R.string.problem_google
    },
)

/** [treeName]: the tree the person was saving, named in the line under the title. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SignInSheet(account: Account, treeName: String?, onDismiss: () -> Unit) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var typing by remember { mutableStateOf(false) }
    var email by remember { mutableStateOf("") }

    ModalBottomSheet(onDismissRequest = { account.dismissProblem(); onDismiss() }) {
        Column(
            Modifier.fillMaxWidth().padding(horizontal = 24.dp).padding(bottom = 24.dp).navigationBarsPadding(),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            when (val s = account.state) {
                is SignIn.LinkSent -> {
                    SheetTitle(stringResource(R.string.signin_sent_title))
                    Text(
                        buildAnnotatedString {
                            append(stringResource(R.string.signin_sent_1))
                            withStyle(SpanStyle(fontWeight = FontWeight.Bold)) { append(s.email) }
                            append(stringResource(R.string.signin_sent_2))
                        },
                        style = MaterialTheme.typography.bodyMedium,
                    )
                }
                is SignIn.Working, is SignIn.Checking -> {
                    CircularProgressIndicator(Modifier.align(Alignment.CenterHorizontally).padding(24.dp))
                }
                else -> {
                    SheetTitle(stringResource(R.string.signin_title))
                    Text(
                        if (treeName != null) stringResource(R.string.signin_sub_named, treeName)
                        else stringResource(R.string.signin_sub),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    Button(onClick = { account.openGoogle(context) }, modifier = Modifier.fillMaxWidth()) {
                        Text(stringResource(R.string.signin_google))
                    }
                    if (!typing) {
                        OutlinedButton(onClick = { typing = true }, modifier = Modifier.fillMaxWidth()) {
                            Text(stringResource(R.string.signin_email))
                        }
                    } else {
                        OutlinedTextField(
                            value = email,
                            onValueChange = { email = it },
                            label = { Text(stringResource(R.string.signin_email_label)) },
                            placeholder = { Text(stringResource(R.string.signin_placeholder)) },
                            singleLine = true,
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                            modifier = Modifier.fillMaxWidth(),
                        )
                        OutlinedButton(
                            onClick = { scope.launch { account.sendLink(email) } },
                            modifier = Modifier.fillMaxWidth(),
                        ) { Text(stringResource(R.string.signin_send)) }
                    }
                    account.problem?.let {
                        Text(problemText(it), color = MaterialTheme.colorScheme.error, style = MaterialTheme.typography.bodySmall)
                    }
                    Text(
                        AnnotatedString.fromHtml(stringResource(R.string.signin_fine)),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
    }
}

/** Signed in: who, sign out, delete. Each step that cannot be undone asks first. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AccountSheet(account: Account, saved: Int, onDismiss: () -> Unit) {
    val scope = rememberCoroutineScope()
    var confirm by remember { mutableStateOf<String?>(null) }
    var failed by remember { mutableStateOf(false) }
    var busy by remember { mutableStateOf(false) }

    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(
            Modifier.fillMaxWidth().padding(horizontal = 24.dp).padding(bottom = 24.dp).navigationBarsPadding(),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            when (confirm) {
                "out" -> {
                    SheetTitle(stringResource(R.string.sign_out_title))
                    Text(stringResource(R.string.sign_out_body), style = MaterialTheme.typography.bodyMedium)
                    Button(
                        onClick = { scope.launch { account.signOut(); onDismiss() } },
                        modifier = Modifier.fillMaxWidth(),
                    ) { Text(stringResource(R.string.sign_out)) }
                    TextButton(onClick = { confirm = null }, modifier = Modifier.fillMaxWidth()) {
                        Text(stringResource(R.string.cancel))
                    }
                }
                "delete" -> {
                    SheetTitle(stringResource(R.string.delete_title))
                    Text(stringResource(R.string.delete_body), style = MaterialTheme.typography.bodyMedium)
                    if (failed) {
                        Text(stringResource(R.string.delete_failed), color = MaterialTheme.colorScheme.error,
                            style = MaterialTheme.typography.bodySmall)
                    }
                    Button(
                        enabled = !busy,
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error),
                        onClick = {
                            busy = true
                            scope.launch {
                                val ok = account.deleteAccount()
                                busy = false
                                if (ok) onDismiss() else failed = true
                            }
                        },
                        modifier = Modifier.fillMaxWidth(),
                    ) { Text(stringResource(R.string.delete)) }
                    TextButton(onClick = { confirm = null; failed = false }, modifier = Modifier.fillMaxWidth()) {
                        Text(stringResource(R.string.cancel))
                    }
                }
                else -> {
                    SheetTitle(stringResource(R.string.account))
                    (account.state as? SignIn.SignedIn)?.email?.let {
                        Text(it, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Text("${stringResource(R.string.want_to_go)}: $saved", style = MaterialTheme.typography.bodyMedium)
                    OutlinedButton(onClick = { confirm = "out" }, modifier = Modifier.fillMaxWidth()) {
                        Text(stringResource(R.string.sign_out))
                    }
                    TextButton(onClick = { confirm = "delete" }, modifier = Modifier.fillMaxWidth()) {
                        Text(stringResource(R.string.delete_account), color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
    }
}
