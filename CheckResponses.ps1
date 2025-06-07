function processfolderresponse($path){
    Write-Output "Processing folder: $path"
    $openaifileresponses = Get-ChildItem $path
    foreach ($oairesponse in $openaifileresponses) {
        #Write-output "Processing response: $oairesponse"
        try {
            $responseContent = Get-Content -Path $oairesponse.FullName -Raw | ConvertFrom-Json
            if($responseContent.ipAccessControlSupported -contains $True){
                Write-Output "True $($oairesponse.Name)"
            }
            else {
                Write-Output "False $($oairesponse.Name)"
            }
        }
        catch {
            Write-Output "Error processing $($oairesponse.FullName)"
        }

    }
    write-output "Finished processing folder: $path"
    write-output "----------------------------------------"
}
processfolderresponse "C:\Local-Projects\arm-schema-checker\workingfolder\responsesSLM"
processfolderresponse "C:\Local-Projects\arm-schema-checker\workingfolder\responses"



