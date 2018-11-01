#!/bin/bash
echo "Enter the Hash file"
read filename
echo "Output file prefix"
read prefix
while read line; do
	    check=$(echo $line | awk -F\$ '{print $2}')
	        if [ "$check" == "1" ] ; then 
			        echo $line >> "$prefix"_MD5.hashes
				    elif [ "$check" == "5" ]; then
					            echo $line >> "$prefix"_SHA256.hashes
						        elif [ "$check" == "6" ]; then
								        echo $line >> "$prefix"_SHA512.hashes
									    elif [ "$check" == "argon2i" ]; then
										            echo $line >> "$prefix"_argon2i.hashes
											        elif [ "$check" == "pbkdf2-sha256" ]; then
													        echo $line >> "$prefix"_pbkdf2-sha256.hashes
														    else
															            echo $line >> "$prefix"_DES.hashes
																        fi
																done < $filename
