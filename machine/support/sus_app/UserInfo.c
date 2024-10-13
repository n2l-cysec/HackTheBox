using System;
using System.Collections;
using System.Diagnostics;
using System.DirectoryServices;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Runtime.Versioning;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using MatthiWare.CommandLine;
using MatthiWare.CommandLine.Abstractions.Command;
using MatthiWare.CommandLine.Core.Attributes;
using UserInfo.Services;

[assembly: CompilationRelaxations(8)]
[assembly: RuntimeCompatibility(WrapNonExceptionThrows = true)]
[assembly: Debuggable(DebuggableAttribute.DebuggingModes.IgnoreSymbolStoreSequencePoints)]
[assembly: AssemblyTitle("UserInfo")]
[assembly: AssemblyDescription("")]
[assembly: AssemblyConfiguration("")]
[assembly: AssemblyCompany("")]
[assembly: AssemblyProduct("UserInfo")]
[assembly: AssemblyCopyright("Copyright ©  2022")]
[assembly: AssemblyTrademark("")]
[assembly: ComVisible(false)]
[assembly: Guid("5a280d0b-9fd0-4701-8f96-82e2f1ea9dfb")]
[assembly: AssemblyFileVersion("1.0.0.0")]
[assembly: TargetFramework(".NETFramework,Version=v4.8", FrameworkDisplayName = ".NET Framework 4.8")]
[assembly: AssemblyVersion("1.0.0.0")]
namespace UserInfo
{
	internal class Program
	{
		private static async Task Main(string[] args)
		{
			CommandLineParser<GlobalOptions> commandLineParser = new CommandLineParser<GlobalOptions>(new CommandLineParserOptions
			{
				AppName = "UserInfo.exe"
			});
			commandLineParser.DiscoverCommands(Assembly.GetExecutingAssembly());
			_ = (await commandLineParser.ParseAsync(args)).HasErrors;
		}
	}
	public class GetUserOptions
	{
		[Name("username")]
		[Required(true)]
		[Description("Username")]
		public string UserName { get; set; }
	}
	public class FindUserOptions
	{
		[Name("first")]
		[Description("First name")]
		public string FirstName { get; set; }

		[Name("last")]
		[Description("Last name")]
		public string LastName { get; set; }
	}
	public class GlobalOptions
	{
		[Name("v", "verbose")]
		[DefaultValue(false)]
		[Description("Verbose output")]
		public bool Verbose { get; set; }
	}
}
namespace UserInfo.Services
{
	internal class Protected
	{
		private static string enc_password = "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E";

		private static byte[] key = Encoding.ASCII.GetBytes("armando");

		public static string getPassword()
		{
			byte[] array = Convert.FromBase64String(enc_password);
			byte[] array2 = array;
			for (int i = 0; i < array.Length; i++)
			{
				array2[i] = (byte)((uint)(array[i] ^ key[i % key.Length]) ^ 0xDFu);
			}
			return Encoding.Default.GetString(array2);
		}
	}
	internal class LdapQuery
	{
		private DirectoryEntry entry;

		private DirectorySearcher ds;

		public LdapQuery()
		{
			//IL_0018: Unknown result type (might be due to invalid IL or missing references)
			//IL_0022: Expected O, but got Unknown
			//IL_0035: Unknown result type (might be due to invalid IL or missing references)
			//IL_003f: Expected O, but got Unknown
			string password = Protected.getPassword();
			entry = new DirectoryEntry("LDAP://support.htb", "support\\ldap", password);
			entry.AuthenticationType = (AuthenticationTypes)1;
			ds = new DirectorySearcher(entry);
		}

		public void query(string first, string last, bool verbose = false)
		{
			//IL_011e: Unknown result type (might be due to invalid IL or missing references)
			try
			{
				if (first == null && last == null)
				{
					Console.WriteLine("[-] At least one of -first or -last is required.");
					return;
				}
				string text = ((last == null) ? ("(givenName=" + first + ")") : ((first != null) ? ("(&(givenName=" + first + ")(sn=" + last + "))") : ("(sn=" + last + ")")));
				if (verbose)
				{
					Console.WriteLine("[*] LDAP query to use: " + text);
				}
				ds.Filter = text;
				ds.PropertiesToLoad.Add("sAMAccountName");
				SearchResultCollection val = ds.FindAll();
				if (val.Count == 0)
				{
					Console.WriteLine("[-] No users identified with that query.");
					return;
				}
				if (verbose)
				{
					string text2 = "[+] Found " + val.Count + " result";
					if (val.Count > 1)
					{
						text2 += "s";
					}
					text2 += ":";
					Console.WriteLine(text2);
				}
				foreach (SearchResult item in val)
				{
					if (verbose)
					{
						Console.Write("       ");
					}
					Console.WriteLine(item.Properties["sAMAccountName"][0]);
				}
			}
			catch (Exception ex)
			{
				Console.WriteLine("[-] Exception: " + ex.Message);
			}
		}

		public void printUser(string username, bool verbose = false)
		{
			try
			{
				if (verbose)
				{
					Console.WriteLine("[*] Getting data for " + username);
				}
				ds.Filter = "sAMAccountName=" + username;
				ds.PropertiesToLoad.Add("pwdLastSet");
				ds.PropertiesToLoad.Add("lastLogon");
				ds.PropertiesToLoad.Add("givenName");
				ds.PropertiesToLoad.Add("sn");
				ds.PropertiesToLoad.Add("mail");
				SearchResult val = ds.FindOne();
				if (val == null)
				{
					Console.WriteLine("[-] Unable to locate " + username + ". Please try the find command to get the user's username.");
					return;
				}
				if (((ReadOnlyCollectionBase)(object)val.Properties["givenName"]).Count > 0)
				{
					Console.WriteLine("First Name:           " + val.Properties["givenName"][0]);
				}
				if (((ReadOnlyCollectionBase)(object)val.Properties["sn"]).Count > 0)
				{
					Console.WriteLine("Last Name:            " + val.Properties["sn"][0]);
				}
				if (((ReadOnlyCollectionBase)(object)val.Properties["mail"]).Count > 0)
				{
					Console.WriteLine("Contact:              " + val.Properties["mail"][0]);
				}
				if (val.Properties.Contains("pwdLastSet"))
				{
					Console.WriteLine("Last Password Change: " + DateTime.FromFileTime((long)val.Properties["pwdLastSet"][0]));
				}
			}
			catch (Exception ex)
			{
				Console.WriteLine("[-] Exception: " + ex.Message);
			}
		}
	}
}
namespace UserInfo.Commands
{
	public class FindUser : Command<GlobalOptions, FindUserOptions>
	{
		public override void OnConfigure(ICommandConfigurationBuilder builder)
		{
			builder.Name("find").Description("Find a user");
		}

		public override async Task OnExecuteAsync(GlobalOptions options, FindUserOptions commandOptions, CancellationToken cancellationToken)
		{
			new LdapQuery().query(commandOptions.FirstName, commandOptions.LastName, options.Verbose);
		}
	}
	public class GetUser : Command<GlobalOptions, GetUserOptions>
	{
		public override void OnConfigure(ICommandConfigurationBuilder builder)
		{
			builder.Name("user").Description("Get information about a user");
		}

		public override async Task OnExecuteAsync(GlobalOptions options, GetUserOptions commandOptions, CancellationToken cancellationToken)
		{
			new LdapQuery().printUser(commandOptions.UserName, options.Verbose);
		}
	}
}
