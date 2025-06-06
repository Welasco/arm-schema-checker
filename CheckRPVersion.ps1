$rpList = get-content .\RPList.txt
$rpFilteredList = @()
foreach($rpListEntry in $rpList){
    $rpListEntryName = "$($rpListEntry.split("/")[0]).json".ToLower()
    if ($rpFilteredList -notcontains $rpListEntryName) {
        $rpFilteredList += $rpListEntryName
    }
}
#$rpFilteredList

$apiVersionFolder = Get-ChildItem .\azure-resource-manager-schemas\schemas -Exclude "*preview*"  | sort-object BaseName -Descending
foreach($rpListEntry in $rpFilteredList){
    $rpListEntryName = $rpListEntry
    foreach ($folder in $apiVersionFolder) {
        $rpFolderList = Get-ChildItem $folder.FullName
        foreach ($rpFile in $rpFolderList) {
            $rpFileName = $rpFile.Name.ToLower()
            if ($rpFileName -eq $rpListEntryName) {
                Write-Host "$($rpFile.FullName)"
                Write-Output "$($rpFile.FullName)" >> .\RPVersionCheck.txt
                $found = $true
                break
            }
        }
        if ($found) {
            $found = $false
            break
        }
    }
}

Get-content .\RPVersionCheck.txt | %{cp $_ .\workingfolder\schemasToValidate}