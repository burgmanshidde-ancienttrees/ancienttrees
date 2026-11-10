// Signing in and the account, each in one bottom sheet (CLAUDE.md, "One sheet for
// every overlay"). The words are the website's sign-in copy
// (site/src/lib/signin-strings.ts) in every language; the route is the iPhone's:
// Google, or an emailed link that brings the person back to the app.

package app.ancienttrees.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextOverflow
import app.ancienttrees.feed.Tree
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
    Text(text, fontFamily = BrandFace, fontWeight = FontWeight.Bold, fontSize = 26.sp, lineHeight = 31.sp)
}

/** Signed in: who, sign out, delete. Each step that cannot be undone asks first. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AccountSheet(
    account: Account,
    hearted: List<Tree>,
    collected: List<Tree>,
    onOpen: (Tree) -> Unit,
    onDismiss: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    var confirm by remember { mutableStateOf<String?>(null) }
    var failed by remember { mutableStateOf(false) }
    var busy by remember { mutableStateOf(false) }

    AppSheet(onDismissRequest = onDismiss) {
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
                    // YOUR TREES: the iPhone's two lanes, Collected and Want to
                    // visit, plain underlined tabs, no counts (Collect.swift).
                    var lane by remember { mutableStateOf(if (collected.isEmpty() && hearted.isNotEmpty()) 1 else 0) }
                    Row(horizontalArrangement = Arrangement.spacedBy(24.dp)) {
                        LaneTab(stringResource(R.string.seen_it_done), lane == 0) { lane = 0 }
                        LaneTab(stringResource(R.string.want_to_visit), lane == 1) { lane = 1 }
                    }
                    val rows = if (lane == 0) collected else hearted
                    LazyColumn(Modifier.fillMaxWidth().heightIn(max = 320.dp)) {
                        items(rows, key = { it.id }) { t ->
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier.fillMaxWidth().clickable { onOpen(t) }.padding(vertical = 8.dp),
                            ) {
                                t.photo?.let { p ->
                                    RemoteImage(p.card, t.name, Modifier.size(52.dp).clip(RoundedCornerShape(10.dp)))
                                    Spacer(Modifier.size(12.dp))
                                }
                                Column(Modifier.weight(1f)) {
                                    Text(t.name, fontFamily = BrandFace, fontWeight = FontWeight.Bold, maxLines = 1,
                                        overflow = TextOverflow.Ellipsis)
                                    Text("${t.commonName} \u00B7 ${t.city}", style = MaterialTheme.typography.bodySmall,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 1,
                                        overflow = TextOverflow.Ellipsis)
                                }
                            }
                        }
                    }
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

@Composable
private fun LaneTab(label: String, on: Boolean, onClick: () -> Unit) {
    Column(Modifier.clickable(onClick = onClick).padding(vertical = 6.dp)) {
        Text(label, fontWeight = if (on) FontWeight.Bold else FontWeight.Medium,
            color = if (on) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurfaceVariant)
        Spacer(Modifier.height(4.dp))
        Box(Modifier.height(2.dp).width(24.dp).background(if (on) MaterialTheme.colorScheme.primary else Color.Transparent))
    }
}

/** The payoff: the tree is in your collection. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CollectedSheet(treeName: String, onDismiss: () -> Unit) {
    AppSheet(onDismissRequest = onDismiss) {
        Column(
            Modifier.fillMaxWidth().padding(horizontal = 24.dp).padding(bottom = 24.dp).navigationBarsPadding(),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            SheetTitle(stringResource(R.string.collected_title, treeName))
            Button(onClick = onDismiss, modifier = Modifier.fillMaxWidth()) { Text(stringResource(R.string.close)) }
        }
    }
}

/** The photograph did not reach us; nothing was kept, so the person tries again. */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CollectFailedSheet(onDismiss: () -> Unit) {
    AppSheet(onDismissRequest = onDismiss) {
        Column(
            Modifier.fillMaxWidth().padding(horizontal = 24.dp).padding(bottom = 24.dp).navigationBarsPadding(),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Text(stringResource(R.string.problem_send), style = MaterialTheme.typography.bodyMedium)
            Button(onClick = onDismiss, modifier = Modifier.fillMaxWidth()) { Text(stringResource(R.string.close)) }
        }
    }
}
