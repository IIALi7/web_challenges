<?php
// reverse_shell.php - SAFE SIMULATED SHELL FOR CTF DEMO
// This file DOES NOT execute system commands. It only simulates outputs
// to demonstrate the risk of allowing uploaded executable scripts.

$cmd = isset($_GET['cmd']) ? trim($_GET['cmd']) : '';
$cmd_l = strtolower($cmd);

function safe($s) {
    return htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
}

$sim_files = [
    'README.txt' => 'This is a demo upload directory. Do not upload real shells here.',
    'notes.txt' => 'Sample notes for the CTF lab.',
    'flag.txt' => 'CSC{SIMULATED_REVERSE_SHELL_FLAG}',
    'secret.doc' => 'Top secret (demo).'
];

function sim_ls($path = '.') {
    global $sim_files;
    $out = "";
    foreach ($sim_files as $name => $content) {
        $size = strlen($content);
        $out .= sprintf("-rw-r--r-- 1 www-data www-data %5d Jan 01 00:00 %s\n", $size, $name);
    }
    return $out;
}

function sim_cat($filename) {
    global $sim_files;
    if (array_key_exists($filename, $sim_files)) {
        return $sim_files[$filename];
    } else {
        return "cat: $filename: No such file or directory";
    }
}

$response = "";
if ($cmd_l === "" || $cmd_l === "help") {
    $response = "Simulated shell (demo). Commands: ls, whoami, pwd, cat <file>, getflag\n";
} elseif ($cmd_l === "ls") {
    $response = sim_ls();
} elseif (strpos($cmd_l, "cat ") === 0) {
    $parts = preg_split('/\s+/', $cmd, 2);
    $file = isset($parts[1]) ? trim($parts[1]) : "";
    $response = sim_cat($file);
} elseif ($cmd_l === "whoami") {
    $response = "www-data";
} elseif ($cmd_l === "pwd") {
    $response = "/var/www/html/uploads";
} elseif ($cmd_l === "getflag") {
    $response = sim_cat('flag.txt');
} else {
    $response = "Simulated execution: " . safe($cmd) . "\n";
    $response .= "Note: This is a SAFE demo. No real commands were executed.\n";
}

header('Content-Type: text/plain; charset=utf-8');
echo $response;
