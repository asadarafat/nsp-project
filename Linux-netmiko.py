import pexpect

child = pexpect.spawn ('ssh root@10.58.23.27',timeout=600)
child.expect ('password:')
child.sendline ('root1234')
child.expect ('#')
print (child.before)

child.sendline ('mkdir sros-20_7_latest')
child.expect ('#')
child.sendline ('cd sros-20_7_latest')
child.expect ('#')
child.sendline ('ls')

print (child.before)

##child.sendline ('scp admin1@135.121.98.254:/nodeImages/7750/20_7/latest_supported/*.* .')

child.sendline ('scp admin1@135.121.98.254:/nodeImages/7750/20_7/latest_supported/sros-vm.qcow2 .')
print (child.before)
child.expect (':')
child.sendline ('yes')
child.expect ('password:')
child.sendline ('admin1')

child.expect(('ETA:'),timeout=60)
print (child.before)
print ('downloading')

child.expect ('#')
child.sendline ('mv sros-vm.qcow2 20_10_latest.qcow2')
child.expect ('#')
print (child.before)