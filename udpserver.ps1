$udpClient = New-Object System.Net.Sockets.UdpClient(12345)
while ($true) {
    $remoteEndPoint = New-Object System.Net.IPEndPoint([System.Net.IPAddress]::Any,0)
    $data = $udpClient.Receive([ref]$remoteEndPoint)
    $msg = [System.Text.Encoding]::UTF8.GetString($data)

    $responseMessage = "Got msg. Sending reply..."
    $responseBytes = [System.Text.Encoding]::UTF8.GetBytes($responseMessage)
    $udpClient.Send($responseBytes, $responseBytes.Length, $remoteEndPoint)
}